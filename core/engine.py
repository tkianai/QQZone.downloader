
import os
import os.path as osp
import requests
import helium as hl
import time
import selenium
from tqdm import tqdm
import warnings
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BackupEngine(object):

    def __init__(self, account, headless=True, web_brower='chrome', save_dir='./results'):

        self.base_url = 'https://user.qzone.qq.com'

        # Album config
        self.album_global_xpath = '//*[@id="js-nav-container"]/div/div[1]/ul/li[1]/a'
        self.album_list_xpath = '//*[@id="js-album-list-noraml"]/div/div/ul/li'
        #self.album_xpath = '//*[@id="js-album-list-noraml"]/div/div/ul/li[{}]/div/div[2]/div/div[2]/a'
        self.album_xpath = '//*[@id="js-album-list-noraml"]/div/div/ul/li[{}]/div/div[1]/a'
        self.image_list_xpath = '//*[@id="js-module-container"]/div[1]/div[3]/div[1]/ul/li'
        self.image_xpath = '//*[@id="js-module-container"]/div[1]/div[3]/div[1]/ul/li[{}]/div/div[1]/a'
        self.image_name_xpath = '//*[@id="js-photo-name"]'
        self.image_src_xpath = '//*[@id="js-img-border"]/img'
        self.next_image_xpath = '//*[@id="js-btn-nextPhoto"]'
        self.image_upload_time_xpath = '//*[@id="_slideView_userinfo"]/div/div/p'
        self.image_comments_xpath = '//*[@id="js-comment-module"]/div/div/div/ul/li'
        self.close_image_within_album_xpath = '//*[@id="js-viewer-main"]/div[1]/a'

        # Post config
        self.post_list_xpath = '//*[@id="msgList"]/li'

        # Leaving msg config
        self.msg_list_xpath = '//*[@id="ulCommentList"]'

        # Diary config
        self.diary_pagination_xpath = '//*[@id="pagination"]'
        self.diary_list_xpath = '//*[@id="listArea"]/ul'
        self.diary_xpath = '//*[@id="listArea"]/ul/li[{}]/div[1]/span/a'
        self.diary_content_xpath = '//*[@id="blogDetailDiv"]'
        self.diary_comment_list_xpath = '//*[@id="commentListDiv"]'
        

        self.account = account
        self.web_brower = web_brower
        self.root_dir = save_dir

        print("Make sure you have logged in qq client!")
        if web_brower == 'chrome':
            hl.start_chrome(self.base_url, headless=headless)
        elif web_brower == 'firefox':
            hl.start_firefox(self.base_url, headless=headless)
        else:
            raise "Unsupported web browser: {}".format(web_brower)
        
        # Login
        hl.click(account)
        # Get web driver
        self.driver = hl.get_driver()
        self.driver.set_window_size(1200, 833)
        self.driver_frame = 'default'
        self.waits_until(
            ['相册', '说说', '留言板', '日志'],
            [hl.Link for _ in range(4)]
        )

    
    def waits_until(self, names, elem_types, timeout_secs=10, interval_secs=0.5):
        if not isinstance(names, (list, tuple)):
            names = [names]
        if not isinstance(elem_types, (list, tuple)):
            elem_types = [elem_types]
        for name, elem_type in zip(names, elem_types):
            hl.wait_until(elem_type(name).exists, timeout_secs=timeout_secs, interval_secs=interval_secs)


    def wait_until_by_attr(self, name, attr='xpath', timeout_secs=10, interval_secs=1):
        filter_fn = None
        if attr == 'id':
            filter_fn = By.ID
        elif attr == 'xpath':
            filter_fn = By.XPATH
        
        element = WebDriverWait(self.driver, timeout_secs, poll_frequency=interval_secs).until(
            EC.presence_of_element_located((filter_fn, name))
        )
        return element


    def click(self, elem, robust=True):
        hl.click(elem)
        if robust:
            time.sleep(1)


    def finished(self):
        hl.kill_browser()


    def save_file(self, url, path):
        if osp.isfile(path):
            pass
        else:
            r = requests.get(url)
            with open(path, 'wb') as w_obj:
                w_obj.write(r.content)

    def switch_to_frame(self, frame_id):
        if frame_id == 'default':
            self.driver.switch_to.default_content()
        else:
            self.driver.switch_to.frame(frame_id)
        self.driver_frame = frame_id


    def download_images(self, with_time=True, with_comment=True):
        """back up images from qq zone
        
        Keyword Arguments:
            with_time {bool} -- saving with the upload time (default: {False})
            with_comment {bool} -- saving with the comments of the image (default: {False})
        """        
        hl.click("相册")
        frame_id = 'tphoto'
        iframe_elem = self.wait_until_by_attr(frame_id, attr='id')
        self.switch_to_frame(frame_id)
        self.wait_until_by_attr(self.album_list_xpath)
        album_elems = self.driver.find_elements_by_xpath(self.album_list_xpath)
        album_num = len(album_elems)
        print("There are {} albums to be downloaded!".format(album_num))

        # For each album
        for i in range(9, album_num + 1):
            # return to album list page
            if i != 1:
                elem = self.wait_until_by_attr(self.album_global_xpath)
                hl.click(elem)
            album_xpath = self.album_xpath.format(i)
            album_elem = self.wait_until_by_attr(album_xpath)
            title = album_elem.get_attribute('title')
            save_dir = osp.join(self.root_dir, "相册", title)
            if not osp.exists(save_dir):
                os.makedirs(save_dir)
            print("Downloading album: {}".format(title))

            # NOTE handle the element is hidden
            # Enter album
            enter_success = False
            trial_times = 0
            while (not enter_success) and (trial_times <= 15):
                try:
                    hl.click(album_elem)
                    enter_success = True
                except :
                    hl.scroll_down(10)
                    print("scrolling down...")
                    trial_times += 1
            try:
                self.wait_until_by_attr(self.image_list_xpath)
            except:
                pass
            image_elems = self.driver.find_elements_by_xpath(self.image_list_xpath)
            image_num = len(image_elems)
            print("There are {} images in {} album".format(image_num, title))
            if image_num == 0:
                continue
            continue

            # Start from the first image
            crawled_data = {}
            j = 1 
            pbar = tqdm(total=image_num)
            while j <= image_num:
                if j == 1:
                    # Find the first image
                    image_xpath = self.image_xpath.format(j)
                    image_elem = self.wait_until_by_attr(image_xpath)
                    hl.click(image_elem)
                    time.sleep(2)

                    # Change driver frame
                    self.switch_to_frame('default')
                
                upload_time = ''
                if with_time:
                    upload_time_elem = self.wait_until_by_attr(self.image_upload_time_xpath)
                    upload_time = upload_time_elem.text

                # Find image name
                name_elem = self.wait_until_by_attr(self.image_name_xpath)
                image_name = str(hash(name_elem.get_attribute('innerHTML') + str(time.time())))
                # Find image url
                src_elem = self.wait_until_by_attr(self.image_src_xpath)
                image_url = src_elem.get_attribute('src')
                # Save the file system
                self.save_file(image_url, osp.join(save_dir, upload_time + '_' + image_name + '.jpg'))
                
                comments = ""
                if with_comment:
                    comment_elems = self.driver.find_elements_by_xpath(self.image_comments_xpath)
                    if len(comment_elems) > 0:
                        for com_elem in comment_elems:
                            comments += com_elem.text
                            comments += '\n'
                        
                        # save to file
                        with open(osp.join(save_dir, upload_time + '_' + image_name + '.txt'), 'w') as w_obj:
                            w_obj.write(comments)

                # NOTE missed
                crawled_data[image_name] = {
                    'upload_time': upload_time,
                    'url': image_url,
                    'comments': comments,
                }

                # Process next image
                j += 1
                pbar.update(1)
                if j <= image_num:
                    # Visualize button(next)
                    hl.hover(src_elem)
                    next_elem = self.wait_until_by_attr(self.next_image_xpath)
                    # Move to next image
                    hl.click(next_elem)
                    time.sleep(2)
            
            # Close current image show page
            with open(osp.join(save_dir, "total_infos.json"), 'w') as w_obj:
                json.dump(crawled_data, w_obj)
            close_elem = self.wait_until_by_attr(self.close_image_within_album_xpath)
            hl.click(close_elem)
            time.sleep(5)


    def download_posts(self):

        save_dir = osp.join(self.root_dir, "说说")
        if not osp.exists(save_dir):
            os.makedirs(save_dir)

        hl.click("说说")
        frame_id = 'app_canvas_frame'
        iframe_elem = self.wait_until_by_attr(frame_id, attr='id')
        self.switch_to_frame(frame_id)
        
        # NOTE it's weak for the judgement of post ending
        last_page_posts = ''
        while True:
            current_page_posts = ''
            self.wait_until_by_attr(self.post_list_xpath)
            post_elems = self.driver.find_elements_by_xpath(self.post_list_xpath)
            for post_elem in post_elems:
                post = post_elem.text
                post = '\n'.join(post.split('\n')[:-1])
                current_page_posts += post
                current_page_posts += '\n' * 3
            
            if current_page_posts == last_page_posts:
                break
            
            # save to file
            with open(osp.join(save_dir, 'post.txt'), 'a') as a_obj:
                a_obj.write(current_page_posts)

            # update
            last_page_posts = current_page_posts
            # move to next page
            hl.click("下一页")
            time.sleep(10)

    def download_leaving_message(self):

        save_dir = osp.join(self.root_dir, "留言板")
        if not osp.exists(save_dir):
            os.makedirs(save_dir)

        hl.click("留言板")
        frame_id = 'tgb'
        iframe_elem = self.wait_until_by_attr(frame_id, attr='id')
        self.switch_to_frame(frame_id)

        # NOTE it's weak for the judgement of message board ending
        last_page_msgs = ''
        while True:
            current_page_msgs = ''
            msg_ul_elem = self.wait_until_by_attr(self.msg_list_xpath)
            msg_elems = msg_ul_elem.find_elements_by_xpath('li')
            for msg_elem in msg_elems:
                msg = msg_elem.text
                current_page_msgs += msg
                current_page_msgs += '\n' * 3

            if current_page_msgs == last_page_msgs:
                break

            # save to file
            with open(osp.join(save_dir, 'leaving_message.txt'), 'a') as a_obj:
                a_obj.write(current_page_msgs)

            # update
            last_page_msgs = current_page_msgs
            # move to next page
            hl.click("下一页")
            time.sleep(10)


    def download_diary(self):
        
        save_dir = osp.join(self.root_dir, "日志")
        if not osp.exists(save_dir):
            os.makedirs(save_dir)

        hl.click("日志")
        frame_id = 'tblog'
        iframe_elem = self.wait_until_by_attr(frame_id, attr='id')
        self.switch_to_frame(frame_id)

        pag_elem = self.wait_until_by_attr(self.diary_pagination_xpath)
        pag_number = []
        for item in pag_elem.text.split(' '):
            try:
                n = int(item)
                pag_number.append(n)
            except:
                pass
        max_page = max(pag_number)

        for _ in range(3, max_page):
            # process each page
            diary_ul_elem = self.wait_until_by_attr(self.diary_list_xpath)
            diary_list_elems = diary_ul_elem.find_elements_by_xpath('li')
            print("There are {} diaries in current page".format(len(diary_list_elems)))

            titles = []
            for i in range(len(diary_list_elems)):
                title_raw = diary_list_elems[i].text.split('\n')[:3]
                title_raw[-1] = title_raw[-1].split(' ')[0]
                title = '_'.join(title_raw)
                title = '_'.join(title.split(' '))
                titles.append(title)

            for i in tqdm(range(len(titles))):
                title = titles[i]
                diary_elem = self.wait_until_by_attr(self.diary_xpath.format(i + 1))
                hl.click(diary_elem)
                time.sleep(5)
                
                diary_content_elem = self.wait_until_by_attr(self.diary_content_xpath)
                comment_list = self.driver.find_elements_by_xpath(self.diary_comment_list_xpath)
                with open(osp.join(save_dir, title + '.txt'), 'w') as w_obj:
                    w_obj.write(diary_content_elem.text)
                    if len(comment_list) > 0:
                        w_obj.write('\n'*3)
                        w_obj.write(comment_list[0].text)

                self.driver.back()
                time.sleep(1)
                self.switch_to_frame(frame_id)

            # Move to next page
            hl.click("下一页")
            time.sleep(5)

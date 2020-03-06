
import os
import os.path as osp
import requests
import helium as hl
import time


class BackupEngine(object):

    def __init__(self, account, web_brower='chrome', save_dir='./results'):

        self.base_url = 'https://user.qzone.qq.com'
        self.album_list_xpath = '//*[@id="js-album-list-noraml"]/div/div/ul/li'
        self.album_xpath = '//*[@id="js-album-list-noraml"]/div/div/ul/li[{}]/div/div[2]/div/div[2]/a'
        self.image_list_xpath = '//*[@id="js-module-container"]/div[1]/div[3]/div[1]/ul/li'
        self.image_xpath = '//*[@id="js-module-container"]/div[1]/div[3]/div[1]/ul/li[{}]/div/div[1]/a'
        self.image_name_xpath = '//*[@id="js-photo-name"]'
        self.image_src_xpath = '//*[@id="js-img-border"]/img'
        self.next_image_xpath = '//*[@id="js-btn-nextPhoto"]'
        self.close_image_within_album_xpath = '//*[@id="js-viewer-main"]/div[1]/a'

        self.account = account
        self.web_brower = web_brower
        self.root_dir = save_dir

        print("Make sure you have logged in qq client!")
        if web_brower == 'chrome':
            hl.start_chrome(self.base_url)
        elif web_brower == 'firefox':
            hl.start_firefox()
        else:
            raise "Unsupported web browser: {}".format(web_brower)
        
        # Login
        hl.click(account)
        # Get web driver
        self.driver = hl.get_driver()
        self.driver_frame = 'default'


    def save_file(self, url, path):
        if osp.isfile(path):
            pass
        else:
            r = requests.get(url)
            with open(path, 'wb') as w_obj:
                w_obj.write(r.content)


    def switch_to_frame(self, frame_name):
        if frame_name == 'default':
            self.driver.switch_to.default_content()
        else:
            self.driver.switch_to.frame(frame_name)
        self.driver_frame = frame_name


    def download_images(self, with_time=False, with_comment=False):
        """back up images from qq zone
        
        Keyword Arguments:
            with_time {bool} -- saving with the upload time (default: {False})
            with_comment {bool} -- saving with the comments of the image (default: {False})
        """        
        hl.click("相册")
        time.sleep(15)
        self.switch_to_frame('app_canvas_frame')
        album_elems = self.driver.find_elements_by_xpath(self.album_list_xpath)
        album_num = len(album_elems)
        print("There are {} albums to be downloaded!".format(album_num))

        # For each album
        for i in range(1, album_num + 1):
            # return to album list page
            if i != 1:
                hl.click("相册")
                time.sleep(15)
            album_xpath = self.album_xpath.format(i)
            album_elem = self.driver.find_element_by_xpath(album_xpath)
            title = album_elem.get_attribute('title')
            save_dir = osp.join(self.root_dir, "相册", title)
            if not osp.exists(save_dir):
                os.makedirs(save_dir)
            print("Downloading album: {}".format(title))

            # TODO handle the element is hidden
            # Enter album
            hl.click(album_elem)
            time.sleep(5)

            image_elems = self.driver.find_elements_by_xpath(self.image_list_xpath)
            image_num = len(image_elems)
            print("There are {} images in {} album".format(image_num, title))

            # Start from the first image
            j = 1 
            while j <= image_num:
                if j == 1:
                    # Find the first image
                    image_xpath = self.image_xpath.format(j)
                    image_elem = self.driver.find_element_by_xpath(image_xpath)
                    hl.click(image_elem)
                    time.sleep(5)

                    # Change driver frame
                    self.switch_to_frame('default')
                
                upload_time = ''
                if with_time:
                    # TODO complete this
                    pass

                # Find image name
                name_elem = self.driver.find_element_by_xpath(self.image_name_xpath)
                image_name = name_elem.get_attribute('innerHTML')
                # Find image url
                src_elem = self.driver.find_element_by_xpath(self.image_src_xpath)
                image_url = src_elem.get_attribute('src')
                # Save the file system
                self.save_file(image_url, osp.join(save_dir, upload_time + '_' + image_name + '.jpg'))

                if with_comment:
                    # TODO complete this
                    pass

                # Process next image
                j += 1
                if j <= image_num:
                    # Visualize button(next)
                    hl.hover(src_elem)
                    next_elem = self.driver.find_element_by_xpath(self.next_image_xpath)
                    # Move to next image
                    hl.click(next_elem)
                    time.sleep(5)
            
            # Close current image show page
            close_elem = self.driver.find_element_by_xpath(self.close_image_within_album_xpath)
            hl.click(close_elem)
            time.sleep(10)
        

    def finished(self):
        hl.kill_browser()


    def download_posts(self):
        pass
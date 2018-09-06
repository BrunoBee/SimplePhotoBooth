import os
from time import sleep
import time
import RPi.GPIO as GPIO
import picamera
import pygame


print('start')

GPIO_BLUE_BUTTON = 13
GPIO_GREEN_BUTTON = 19
GPIO_YELLOW_BUTTON = 26
GPIO_EXIT_BUTTON = 6
GPIO_SHUTDOWN_BUTTON = 5
DEBOUNCE_TIME = 0.05 

GPIO_BLUE_LED = 21
GPIO_GREEN_LED = 20
GPIO_YELLOW_LED = 16

GPIO_LIGHT_PREPARE_1 = 12
GPIO_LIGHT_PREPARE_2 = 7
GPIO_LIGHT_PREPARE_3 = 8
GPIO_LIGHT_PREPARE_4 = 25

yellow_blink = 'aus'
blue_blink = 'aus'
green_blink = 'aus'

high_res_w = 1296 # width of high res image, if taken
high_res_h = 972 # height of high res image, if taken

#############################
### Variables that Change ###
#############################
# Do not change these variables, as the code will change it anyway
##transform_x = 1280 # how wide to scale the jpg when replaying
##transfrom_y = 1024 # how high to scale the jpg when replaying
transform_x = 1280 # how wide to scale the jpg when replaying
transfrom_y = 1024 # how high to scale the jpg when replaying
offset_x = 0 # how far off to left corner to display photos
offset_y = 0 # how far off to left corner to display photos

picture_size_x = 853
picture_size_y = 853


####################
### Other Config ###
####################
real_path = os.path.dirname(os.path.realpath(__file__))

# initialize pygame
pygame.init()
pygame.display.set_mode((transform_x, transfrom_y))
screen = pygame.display.get_surface()
pygame.display.set_caption('Photo Booth Pics')
#pygame.mouse.set_visible(False) #hide the mouse cursor
#pygame.display.toggle_fullscreen()

camera = picamera.PiCamera()
camera.rotation = 90
camera.brightness = 55

printer_name = "Canon_SELPHY_CP1300"
    
def init_GPIO():
    

    #set which notation to use (BCM = GPIO-Pins)
    GPIO.setmode(GPIO.BCM)

    # Configuration of ports
    GPIO.setup(GPIO_BLUE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(GPIO_GREEN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(GPIO_YELLOW_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(GPIO_EXIT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(GPIO_SHUTDOWN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    GPIO.setup(GPIO_BLUE_LED, GPIO.OUT)
    GPIO.setup(GPIO_GREEN_LED, GPIO.OUT)   
    GPIO.setup(GPIO_YELLOW_LED, GPIO.OUT)
    GPIO.setup(GPIO_LIGHT_PREPARE_1, GPIO.OUT)
    GPIO.setup(GPIO_LIGHT_PREPARE_2, GPIO.OUT)
    GPIO.setup(GPIO_LIGHT_PREPARE_3, GPIO.OUT)
    GPIO.setup(GPIO_LIGHT_PREPARE_4, GPIO.OUT)


# switch all ports off
    GPIO.output(GPIO_BLUE_LED, GPIO.HIGH)
    GPIO.output(GPIO_GREEN_LED, GPIO.HIGH)
    GPIO.output(GPIO_YELLOW_LED, GPIO.HIGH)
    GPIO.output(GPIO_LIGHT_PREPARE_1, GPIO.HIGH)
    GPIO.output(GPIO_LIGHT_PREPARE_2, GPIO.HIGH)
    GPIO.output(GPIO_LIGHT_PREPARE_3, GPIO.HIGH)
    GPIO.output(GPIO_LIGHT_PREPARE_4, GPIO.HIGH)
    
##    CAMERA = picamera.PiCamera()
##    CAMERA.rotation = 0
##    CAMERA.annotate_text_size = 80
##    CAMERA.resolution = (PHOTO_W, PHOTO_H)
##    CAMERA.hflip = CAMERA_HFLIP



def show_on_screen(picfile):
    print(picfile)
    #layer 1 - unvisible or transparent 2 - Cam, 3 vilsible
    

def flash_light(on_off):
    print('FLASHHHH*******')

def cam_prepare():
    print('prepare cam')
          #flip, size....

def show_mirror(time):

    camera.hflip = True # preview a mirror image
    camera.start_preview(resolution=(picture_size_y,picture_size_y)) # start preview at low res but the right ratio
    sleep(time)
    camera.hflip = False # flip back when taking photo
    camera.stop_preview()
    clear_screen()



    
def take_picture():
    print('smile for picture')
##    show_picture(real_path + '/systempic/smile.jpg')
    now = time.strftime("%Y-%m-%d-%H-%M-%S") #get the current date and time for the start of the filename
    print('cam on')
    


 #   camera.hflip = True # preview a mirror image
  #  camera.start_preview(resolution=(transform_x,transfrom_y)) # start preview at low res but the right ratio
    sleep(2) #warm up camera
    filename = real_path + '/OMI-' + now + '.jpg'
    camera.hflip = False # flip back when taking photo
    #camera.capture(filename)
    camera.capture(filename, resize=(picture_size_x, picture_size_y))
    print(filename)
    show_picture(real_path + '/systempic/click.jpg')
    sleep(1)
    camera.stop_preview()
    clear_screen()

    return filename

# display one image on screen
def show_picture(image_path):

    print('look at this fine picture')

    # clear the screen
    screen.fill( (0,0,0) )

    # load the image
    img = pygame.image.load(image_path)
    img = img.convert() 

    # set pixel dimensions based on image
 #   set_demensions(img.get_width(), img.get_height())

    # rescale the image to fit the current display
    img = pygame.transform.scale(img, (transform_x,transfrom_y))
    screen.blit(img,(offset_x,offset_y))
    pygame.display.flip()

# display a blank screen
def clear_screen():
    screen.fill( (0,0,0) )
    pygame.display.flip()

    
def select_picture():
    selection = wait_on_pressed_button('an', 'an', 'an')

    show_picture(real_path + '/systempic/questions.png')
    return selection

def print_picture(filename):
    print('printing....: lp -d ' + printer_name + ' ' + filename)
    show_picture(real_path + '/systempic/printing.jpg')
    os.system('lp -d ' + printer_name + ' ' + filename)
    
def save_picture():
    return

def wait_on_pressed_button(yellow_blink, blue_blink, green_blink):

#Use falling edge detection to see if button is being pushed in
    GPIO.add_event_detect(GPIO_BLUE_BUTTON, GPIO.FALLING)
    GPIO.add_event_detect(GPIO_GREEN_BUTTON, GPIO.FALLING)
    GPIO.add_event_detect(GPIO_YELLOW_BUTTON, GPIO.FALLING)
    GPIO.add_event_detect(GPIO_EXIT_BUTTON, GPIO.FALLING)
    GPIO.add_event_detect(GPIO_SHUTDOWN_BUTTON, GPIO.FALLING)


    if blue_blink == 'an':
        GPIO.output(GPIO_BLUE_LED, GPIO.LOW)
    if green_blink == 'an':                    
        GPIO.output(GPIO_GREEN_LED, GPIO.LOW)
    if yellow_blink == 'an':                    
        GPIO.output(GPIO_YELLOW_LED, GPIO.LOW)

    print('warte auf Button')
    blink_time = 100
    button_light = False
    blink_count = 0
    while True:
        pressed_button = 'leer'
    
        if GPIO.event_detected(GPIO_BLUE_BUTTON):
            sleep(DEBOUNCE_TIME)
            if GPIO.input(GPIO_BLUE_BUTTON) == 0:
                pressed_button = 'blue'
           
        if GPIO.event_detected(GPIO_GREEN_BUTTON):
            sleep(DEBOUNCE_TIME)
            if GPIO.input(GPIO_GREEN_BUTTON) == 0:
                pressed_button = 'green'
                            
        if GPIO.event_detected(GPIO_YELLOW_BUTTON):
            sleep(DEBOUNCE_TIME)
            if GPIO.input(GPIO_YELLOW_BUTTON) == 0:
                pressed_button = 'yellow'

        if GPIO.event_detected(GPIO_EXIT_BUTTON):
            sleep(DEBOUNCE_TIME)
            if GPIO.input(GPIO_EXIT_BUTTON) == 0:
                pressed_button = 'exit'
                end_booth()
                raise SystemExit

        if GPIO.event_detected(GPIO_SHUTDOWN_BUTTON):
            sleep(DEBOUNCE_TIME)
            if GPIO.input(GPIO_SHUTDOWN_BUTTON) == 0:
                pressed_button = 'exit'
                end_booth()
                shutdown()
                raise SystemExit
           
            
        #    print('pressed_button ' +  pressed_button)

        if pressed_button == 'blue':

            GPIO.output(GPIO_GREEN_LED, GPIO.HIGH)
            GPIO.output(GPIO_YELLOW_LED, GPIO.HIGH)
        
            GPIO.remove_event_detect(GPIO_BLUE_BUTTON)                
            GPIO.remove_event_detect(GPIO_GREEN_BUTTON)         
            GPIO.remove_event_detect(GPIO_YELLOW_BUTTON)
            GPIO.remove_event_detect(GPIO_EXIT_BUTTON)
            GPIO.remove_event_detect(GPIO_SHUTDOWN_BUTTON)
            
            return pressed_button
        
        if pressed_button == 'green':

            GPIO.output(GPIO_BLUE_LED, GPIO.HIGH)
            GPIO.output(GPIO_YELLOW_LED, GPIO.HIGH)
        
            GPIO.remove_event_detect(GPIO_BLUE_BUTTON)                
            GPIO.remove_event_detect(GPIO_GREEN_BUTTON)         
            GPIO.remove_event_detect(GPIO_YELLOW_BUTTON)
            GPIO.remove_event_detect(GPIO_EXIT_BUTTON)
            GPIO.remove_event_detect(GPIO_SHUTDOWN_BUTTON)
            
            return pressed_button

        if pressed_button == 'yellow':

            GPIO.output(GPIO_BLUE_LED, GPIO.HIGH)
            GPIO.output(GPIO_GREEN_LED, GPIO.HIGH)
        
            GPIO.remove_event_detect(GPIO_BLUE_BUTTON)                
            GPIO.remove_event_detect(GPIO_GREEN_BUTTON)         
            GPIO.remove_event_detect(GPIO_YELLOW_BUTTON)
            GPIO.remove_event_detect(GPIO_EXIT_BUTTON)
            GPIO.remove_event_detect(GPIO_SHUTDOWN_BUTTON)
            
            return pressed_button
                  
##        blink_count = blink_count + 1
##
##        print(blink_count)
##
##        if blink_count == blink_time:
##            if button_light == False:
##                if blue_blink == 'an':
##                    GPIO.output(GPIO_BLUE_LED, GPIO.LOW)
##                if green_blink == 'an':                    
##                    GPIO.output(GPIO_GREEN_LED, GPIO.LOW)
##                if yellow_blink == 'an':                    
##                    GPIO.output(GPIO_YELLOW_LED, GPIO.LOW)
##
##                button_light = True
##
##            elif button_light == True:
##                GPIO.output(GPIO_BLUE_LED, GPIO.HIGH)
##                GPIO.output(GPIO_GREEN_LED, GPIO.HIGH)
##                GPIO.output(GPIO_YELLOW_LED, GPIO.HIGH)
##                button_light = False
##                
##            blink_count = 0    

def end_booth():
    print('Goodbye')
    GPIO.cleanup()
    pygame.display.quit
    pygame.quit()
    camera.close()
    
def shutdown():
    #end_booth():
    os.system('shutdown -h now')

def main():
    
    init_GPIO()
            
    GPIO.remove_event_detect(GPIO_BLUE_BUTTON)                
    GPIO.remove_event_detect(GPIO_GREEN_BUTTON)         
    GPIO.remove_event_detect(GPIO_YELLOW_BUTTON)
    GPIO.remove_event_detect(GPIO_EXIT_BUTTON)
    GPIO.remove_event_detect(GPIO_SHUTDOWN_BUTTON)
    while True:
        print('starte sub')

        print('starte sub: ' + real_path + '/systempic/start.jpg')
        show_picture(real_path + "/systempic/start.jpg")
        #show_on_screen('intro')

        yellow_blink = 'an'
        blue_blink =  'an'
        green_blink = 'an'

        countdown_steps = 5
        blink_time = 5
        
        pressed_button = wait_on_pressed_button(yellow_blink, blue_blink, green_blink )

        if pressed_button == 'blue':
            show_picture(real_path + '/systempic/disclamer.jpg')
            sleep(10)
        if pressed_button == 'yellow':
            show_picture(real_path + '/systempic/disclamer.jpg')
            show_mirror(15)
           
        if pressed_button == 'green':
            show_picture(real_path + '/systempic/prepare.jpg')
            sleep(2)
            show_mirror(6)
            sleep(2)
            show_on_screen('schaut in das blaue licht')
            show_picture(real_path + '/systempic/lookintothelight.png')        
            GPIO.output(GPIO_BLUE_LED, GPIO.LOW)
            GPIO.output(GPIO_GREEN_LED, GPIO.HIGH)
           
            for countdown in range(countdown_steps, 0, -1):
                sleep(1)
                show_picture(real_path + '/systempic/count' + str(countdown) + '.jpg')
                if countdown == 1:
                    GPIO.output(GPIO_LIGHT_PREPARE_1, GPIO.LOW)
                if countdown == 2:
                    GPIO.output(GPIO_LIGHT_PREPARE_2, GPIO.LOW)
                if countdown == 3:
                    GPIO.output(GPIO_LIGHT_PREPARE_3, GPIO.LOW)
                if countdown == 4:
                    GPIO.output(GPIO_LIGHT_PREPARE_4, GPIO.LOW)
    
            flash_light(True)

            filename = take_picture()         
            GPIO.output(GPIO_BLUE_LED, GPIO.HIGH)
            GPIO.output(GPIO_LIGHT_PREPARE_1, GPIO.HIGH)
            sleep(0.5)
            GPIO.output(GPIO_LIGHT_PREPARE_2, GPIO.HIGH)
            sleep(0.5)
            GPIO.output(GPIO_LIGHT_PREPARE_3, GPIO.HIGH)
            sleep(0.5)
            GPIO.output(GPIO_LIGHT_PREPARE_4, GPIO.HIGH)
 
            show_picture(real_path + '/systempic/letshavelook.jpg')
            show_picture(filename)
            sleep(5)
            show_picture(real_path + '/systempic/questions.png')
            selection = select_picture()
            if selection == 'blue':
                
                save_picture() 
                show_picture(real_path + '/systempic/saved.jpg')
                sleep(2)                
            if selection == 'green':
                print('printing')
                show_picture(real_path + '/systempic/printing.jpg')
                print_picture(filename)              
                sleep(2)
            if selection == 'yellow':
                save_picture()
                os.remove(filename)
                show_picture(real_path + '/systempic/deleted.jpg')
                sleep(2)
        

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        end_booth()

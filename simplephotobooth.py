from time import sleep
import os



print('start')

yellow_blink = 'aus'
blue_blink =  'aus'
green_blink = 'aus'

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def show_on_screen(picfile):
    print(picfile)
    #layer 1 - unvisible or transparent 2 - Cam, 3 vilsible
    

def flash_light(on_off):
    print('FLASHHHH*******')

def cam_prepare():
    print('prepare cam')
          #flip, size....

def cam_activate():
    print('cam on')

def take_picture():
    print('smile for picture')

def show_picture():
    print('look at this fine picture')
    
def select_picture():
    selection = wait_on_pressed_button('an', 'an', 'an')
    show_on_screen('Print, Save; delete')
    return selection

def print_picture():
    print('printing....')

def save_picture():
    return

def wait_on_pressed_button(yellow_blink, blue_blink, green_blink):
    blink_time = 10
    button_light = False
    blink_count = 0
    while True:
        yellow_button_is_pressed = None
        blue_button_is_pressed = None
        green_button_is_pressed = None

        abfrage = input('y/b/g: ')
        print(abfrage)

        if abfrage == 'y':
            print('aus' + 'aus' + 'aus')
            return abfrage            

        if abfrage == 'b':
            print('aus' + 'aus' + 'aus')
            return abfrage            

        if abfrage == 'g':
            print('aus' + 'aus' + 'aus')
            return abfrage

        if abfrage == 'x':
            raise SystemExit
        
        blink_count = blink_count + 1

        print(blink_count)

        if blink_count == blink_time:
            if button_light == False:
                button_light = True
                print(yellow_blink + blue_blink + green_blink)
            elif button_light == True:
                button_light = False
                print('aus' + 'aus' + 'aus')
            blink_count = 0    

def main():
    while True:
        print('starte sub')
        show_on_screen('intro')

        yellow_blink = 'aus'
        blue_blink=  'an'
        green_blink = 'an'

        countdown_steps = 2
        blink_time = 5
        
        pressed_button = wait_on_pressed_button(yellow_blink, blue_blink, green_blink )

        if pressed_button == 'b':
            show_on_screen('disclaimer')
        if pressed_button == 'g':
            show_on_screen('gleichgehtslos')
            sleep(2)
            show_on_screen('macht euch bereit')
            sleep(2)
            show_on_screen('-----------------')
            sleep(2)
            show_on_screen('schaut in das blaue licht')
            
            for countdown in range(countdown_steps, 0, -1):
                for blink_count in range(1, blink_time):
                    print('aus' + 'an' + 'aus')
                    sleep(1)
                    print('aus' + 'aus' + 'aus')
                show_on_screen('countdown' + str(countdown) + '.jpg')
                cls()
                #countdown_steps = countdown_steps -1
                
            flash_light(True)
            cam_activate()
            sleep(2)
            take_picture()
            sleep(2)
            show_picture()
            sleep(2)
            selection = select_picture()
            if selection == 'y':
                print_picture()
            if selection == 'b':
                print('delete')
            if selection == 'g':
                save_picture()
            
        

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print('Goodbye')

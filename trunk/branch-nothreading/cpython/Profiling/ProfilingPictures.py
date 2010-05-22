import cProfile
from media import *

tests = 500
pic = create_picture(1000, 1000)
newcolor = create_color(0, 0, 255)

def test_create_picture():
    print "Testing create_picture"
    for i in range(1, tests):
        pic_new = create_picture(500, 500);
        
def test_load_picture():
    print "Testing load_picture"
    for i in range(1, tests):
        pic_temp = load_picture("resources/images/barbara.jpg")
        
def test_crop_picture():
    print "Testing crop_picture"
    pic_new = create_picture(1000, 1000)
    for i in range(1, tests):
        crop_picture(pic_new, 1, 1, get_width(pic_new)-1, get_height(pic_new)-1)
        
def test_get_pixel():
    print "Testing get_pixel"
    for i in range(1, tests):
        pixel = get_pixel(pic, 10, 10)
        
def test_get_pixels():
    print "Testing get_pixels"
    for i in range(1, tests):
        pixel_list = get_pixels(pic)
        
def test_get_width():
    print "Testing get_width"
    for i in range(1, tests):
        pic_new = create_picture(i, i+10)
        width = get_width(pic_new)
        
def test_get_height():
    print "Testing get_height"
    for i in range(1, tests):
        pic_new = create_picture(i, i+10)
        height = get_height(pic_new)
        
def test_show():
    print "Testing show"
    for i in range(1, tests):
        show(pic)

def test_show_external():
    print "Testing show_external"
    for i in range(1, tests):
        show_external(pic)
        
def test_update():
    print "Testing update"
    for i in range(1, tests):
        update(pic)
        
def test_close():
    print "Testing close"
    for i in range(1, tests):
        pic_new = load_picture("resources/images/barbara.jpg")
        show(pic_new)
        close(pic_new)
        
def run_profiling_tests_pictures():
    cProfile.run("test_create_picture()")
    cProfile.run("test_load_picture()")
    cProfile.run("test_crop_picture()")
    cProfile.run("test_get_pixel()")
    cProfile.run("test_get_pixels()")
    cProfile.run("test_get_height()")
    cProfile.run("test_get_width()")
    print "Most picture-related functions have been profiled. Run run_profiling_tests_display to see results of display-heavy functions."
    
def run_profiling_tests_display():
    #cProfile.run("test_show_external()")
    #cProfile.run("test_show()")
    #cProfile.run("test_close()")
    cProfile.run("test_update()")
    print "Display-heavy functions have been profiled."

def test_add_line():
    print "Testing add_line"
    pic_new = create_picture(500, 500)
    for i in range(1, tests):
        add_line(pic_new, i, i, i+10, i, newcolor)
        
def test_add_text():
    print "Testing add_text"
    pic_new = create_picture(500, 500)
    for i in range(1, tests):
        text = "Test text"
        add_text(pic_new, i, i, text, newcolor)

def test_add_rect():
    print "Testing add_rect"
    pic_new = create_picture(500, 500)
    for i in range(1, tests):
        add_rect(pic_new, i, i, 10, 10, newcolor)
        
def test_add_rect_filled():
    print "Testing add_rect_filled"
    pic_new = create_picture(500, 500)
    for i in range(1, tests):
        add_rect_filled(pic_new, i, i, 10, 10, newcolor)
        
def test_add_oval():
    print "Testing add_oval"
    pic_new = create_picture(500, 500)
    for i in range(1, tests):
        add_oval(pic_new, i, i, 10, 10, newcolor)

def test_add_oval_filled():
    print "Testing add_oval_filled"
    pic_new = create_picture(500, 500)
    for i in range(1, tests):
        add_oval_filled(pic_new, i, i, 10, 10, newcolor)

def test_add_polygon():
    print "Testing add_polygon"
    pic_new = create_picture(500, 500)
    for i in range(1, tests):
        point_list = [i, i, i+5, i, i+10, i+5, i+5, i+10]
        add_polygon(pic_new, point_list, newcolor)

def test_add_polygon_filled():
    print "Testing add_polygon_filled"
    pic_new = create_picture(500, 500)
    for i in range(1, tests):
        point_list = [i, i, i+5, i, i+10, i+5, i+5, i+10]
        add_polygon_filled(pic_new, point_list, newcolor)
        
        
def run_profiling_tests_geometry():
    cProfile.run("test_add_line()")
    cProfile.run("test_add_text()")
    cProfile.run("test_add_rect()")
    cProfile.run("test_add_rect_filled()")
    cProfile.run("test_add_oval()")
    cProfile.run("test_add_oval_filled()")
    cProfile.run("test_add_polygon()")
    cProfile.run("test_add_polygon_filled()")
    
def test_set_red():
    print "Testing set_red"
    pic_new = create_picture(500, 500)
    for i in range(1, tests):
        pixel = get_pixel(pic_new, i, i)
        set_red(pixel, i % 255)
        
def test_get_red():
    print "Testing get_red"
    for i in range(1, tests):
        pixel = get_pixel(pic, 15, 15)
        red = get_red(pixel)

def test_set_green():
    print "Testing set_green"
    pic_new = create_picture(500, 500)
    for i in range(1, tests):
        pixel = get_pixel(pic_new, i, i)
        set_green(pixel, i % 255)
        
def test_get_green():
    print "Testing get_green"    
    for i in range(1, tests):
        pixel = get_pixel(pic, 15, 15)
        red = get_green(pixel)

def test_set_blue():
    print "Testing get_blue"    
    pic_new = create_picture(500, 500)
    for i in range(1, tests):
        pixel = get_pixel(pic_new, i, i)
        set_blue(pixel, i % 255)
        
def test_get_blue():
    print "Testing get_blue"    
    for i in range(1, tests):
        pixel = get_pixel(pic, 15, 15)
        red = get_blue(pixel)

def test_get_color():
    print "Testing get_color"    
    for i in range(1, tests):
        pixel = get_pixel(pic, 15, 15)
        color = get_color(pixel)

def test_set_color():
    print "Testing set_color"
    for i in range(1, tests):
        pixel = get_pixel(pic, 15, 15)
        set_color(pixel, newcolor)

def test_get_x():
    print "Testing get_x"
    pixel = get_pixel(pic, 20, 20)
    for i in range(1, tests):
        x = get_x(pixel)
        
def test_get_y():
    print "Testing get_y"
    pixel = get_pixel(pic, 20, 20)
    for i in range(1, tests):
        x = get_y(pixel)
        
def test_distance():
    print "Testing distance"
    color1 = create_color(100, 100, 100)
    color2 = create_color(255, 255, 255)
    for i in range(1, tests):
        dist = distance(color1, color2)

def test_darken():
    print "Testing darken"
    color1 = create_color(255, 255, 255)
    for i in range(1, tests):
        darken(color1)
        
def test_lighten():
    print "Testing lighten"
    color1 = create_color(1, 1, 1)
    for i in range(1, tests):
        lighten(color1)
        
def test_create_color():
    print "Testing create_color"
    for i in range(1, tests):
        color = create_color(i % 255, i % 255, i % 255)
        
def run_profiling_tests_color():
    cProfile.run("test_set_red()")
    cProfile.run("test_get_red()")
    cProfile.run("test_set_green()")
    cProfile.run("test_get_green()")
    cProfile.run("test_set_blue()")
    cProfile.run("test_get_blue()")
    cProfile.run("test_set_color()")
    cProfile.run("test_get_color()")
    cProfile.run("test_get_x()")
    cProfile.run("test_get_y()")
    cProfile.run("test_distance()")
    cProfile.run("test_darken()")
    cProfile.run("test_lighten()")
    cProfile.run("test_create_color()")
    
#run_profiling_tests_pictures()    
#run_profiling_tests_display()
#run_profiling_tests_geometry()
#run_profiling_tests_color()
import pygame
import random
import math

pygame.init()


class DrawInformation:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BG_COLOR = WHITE
    
    GREY_GRADIENTS = [
        (128, 128, 128), # Grey
        (147, 147, 150), # Light Grey
        (169, 169, 171), # Light Grey 2
        (185, 185, 189), # Light Grey 3
    ]
    
    FONT = pygame.font.SysFont("comicsans", 25)
    LARGE_FONT = pygame.font.SysFont('comicsans', 35)
    
    SIDE_PAD = 100
    TOP_PAD = 150
    
    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Visualizer")
        self.set_list(lst)
        
        
    def set_list(self, lst):
        self.lst = lst
        self.min_val, self.max_val = min(lst), max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD / 2
  
  
def bubble_sort(draw_info: DrawInformation, ascending=True):
    lst = draw_info.lst
    
    for i in range(len(lst) - 1):
        for j in range(len(lst) - i - 1):
            num1 = lst[j]
            num2 = lst[j + 1]
            
            if num1 > num2 and ascending or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = num2, num1
                draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
                yield True
       
def insertion_sort(draw_info: DrawInformation, ascending=True):
    lst = draw_info.lst
    
    for i in range(len(lst)):
        current = lst[i]
        
        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending
            
            if not ascending_sort and not descending_sort:
                break
            
            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i: draw_info.GREEN, i-1: draw_info.RED}, True)
            yield True
            
def mergeSort(draw_info: DrawInformation, ascending=True):
    lst = draw_info.lst

    def mergeSortRec(start, end):
        if end - start > 1:
            middle = (start + end) // 2

            yield from mergeSortRec(start, middle)
            yield from mergeSortRec(middle, end)
            left = lst[start:middle]
            right = lst[middle:end]

            a = 0
            b = 0
            c = start

            while a < len(left) and b < len(right):
                if left[a] < right[b]:
                    lst[c] = left[a]
                    a += 1
                else:
                    lst[c] = right[b]
                    b += 1
                c += 1
                draw_list(draw_info, {a: draw_info.GREEN, b: draw_info.RED}, True)

            while a < len(left):
                lst[c] = left[a]
                a += 1
                c += 1
                draw_list(draw_info, {a: draw_info.GREEN, b: draw_info.RED}, True)

            while b < len(right):
                lst[c] = right[b]
                b += 1
                c += 1
                draw_list(draw_info, {a: draw_info.GREEN, b: draw_info.RED}, True)
            
            yield True

    yield from mergeSortRec(0, len(lst))         
            
            
        
def generare_list(n, min_val, max_val):
    lst = []
    
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
        
    return lst
        

def draw(draw_info: DrawInformation, algo_name, ascending):
    draw_info.window.fill(draw_info.BG_COLOR)
    draw_list(draw_info)
    
    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'} ", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 0))
    
    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 50))

    sorting = draw_info.FONT.render("1 - Insertion Sort | 2 - Bubble Sort | 3 - Merge Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 80))
    
    pygame.display.update()
    

def draw_list(draw_info: DrawInformation, color_positions={}, clear_bg=False):
    lst = draw_info.lst
    
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width, draw_info.height)
        pygame.draw.rect(draw_info.window, draw_info.BG_COLOR, clear_rect)
    
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height - draw_info.block_height
        
        color = draw_info.GREY_GRADIENTS[i % 4]
        
        if i in color_positions:
            color = color_positions[i]
        
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()
    

algorithms = {
    1: ("Insertion Sort", insertion_sort),
    2: ("Bubble Sort", bubble_sort),
    3: ("Merge Sort", mergeSort)
}

def main():
    run = True
    clock = pygame.time.Clock()
    FPS = 120
    
    sorting = False
    ascending = True
    sorting_algorithm = algorithms[2][1]
    sorting_algo_name = algorithms[2][0]
    sorting_algorithm_generator = None
    
    n = 120
    min_val, max_val = 1, 100
    
    lst = generare_list(n, min_val, max_val)
    draw_info = DrawInformation(900, 700, lst)
    
    while run:
        clock.tick(FPS)
        
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type != pygame.KEYDOWN:
                continue
            
            if event.key == pygame.K_r and not sorting:
                lst = generare_list(n, min_val, max_val)
                draw_info.set_list(lst)
            elif event.key == pygame.K_SPACE:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_1 and not sorting:
                sorting_algorithm = algorithms[1][1]
                sorting_algo_name = algorithms[1][0]
            elif event.key == pygame.K_2 and not sorting:
                sorting_algorithm = algorithms[2][1]
                sorting_algo_name = algorithms[2][0]
            elif event.key == pygame.K_3 and not sorting:
                sorting_algorithm = algorithms[3][1]
                sorting_algo_name = algorithms[3][0]
                
                 
                
    pygame.quit()
    
    
if __name__ == '__main__':
    main()
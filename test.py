# import pygame
# screen = pygame.display.set_mode((1000, 1000))
# with open('Back\\board_grid', 'r') as r:
#     data = r.readlines()
#     for i in data:
#         if '#' in i:
#             continue
#         i = i.rstrip()
#         x_y = i.split(',')
#         coor = list()
#         for j in x_y:
#             j = j.strip(' ')
#             coor.append(j)
#         print(coor)
#         rect = pygame.Rect(float(coor[0]), float(coor[1]), float(coor[2]), float(coor[3]))
#         pygame.draw.rect(screen, (255, 0, 0), rect, 1)
#         pygame.display.flip()


print('Ola'.ljust(512, '='))
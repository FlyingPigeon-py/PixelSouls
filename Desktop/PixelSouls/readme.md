# Добро пожаловать в Souls Pixel

Хочу представить вам **PixelSouls**
Это игра сделанная на PyGame.

# Main goals

Должна быть реализована работа со спрайтами, анимациями, базами данных. В задумке было создать простенький пошаговый рогалик

Всё это должно быть выполнено, при помощи **PyGame**.

## Gameplay
Ваш персонаж находиться на клеточном поле, с множеством  врагов, ваша задача довести его до выхода. Попутно вы можете собирать разнообразное оружие и предметы.
!![](https://i.imgur.com/P14prtk.png)
![enter image description here](https://i.imgur.com/GcTLqQS.png)

## How it works

Если я буду объяснять каждый элемент игры, то мы здесь останемся надолго, поэтому я коротко опишу как оно работает

У нас есть один игровой цикл, в котором находятся функции, для отрисовки, и улавливания event

    while info.running:  
      for event in pygame.event.get():  
      if event.type == pygame.QUIT:  
      info.running = False    
    if STOPPED_PLAYING == event.type:  
      pygame.mixer.music.load(rf"../Sounds\Medieval Vol. 2 {random.randint(1, 8)}.mp3")  
      pygame.mixer.music.play()         
                            
     if info.isPlay and board.get_player().isAlive:  
      game_event()  
      elif info.isMenu:  
      info.menu_w.widget_event(event)  
      elif type(info.play_end) != bool:  
      info.play_end.widget_event(event)  
                   
     if info.isSetting:  
      info.setting_w.widget_event(event)  
      if info.play_stop and not info.isSetting:  
      pause_w.widget_event(event)  
      screen.fill((0, 0, 0))  
      if info.isPlay:  
      make_a_move(board)   
     make_attack(board, game_sound, text, effects)          
     game_draw()            
          
     if info.play_end:  
      if type(info.play_end) == bool:  
      play_end_create()  
      info.play_end.move(0, 700)  
      game_sound.sound_dash.play()  
      dark = 0  
      velocity = 0  
      else:  
      dark_screen((0, 0, 0), dark)  
                   
     if info.play_end.direction:  
      if (info.play_end.y - velocity) < 0:  
      info.play_end.move(0, -info.play_end.y)  
      else:  
      info.play_end.move(0, -velocity)  
      velocity += 5  
      if info.play_end.y <= 0:  
      info.play_end.direction = False  
      velocity = 0  
      
      if dark < 150:  
      dark += 5  
      info.play_end.draw(screen)  
      if info.isMenu:  
      if not info.isSetting:  
      if info.menu_w.x <= 900:  
      info.menu_w.direction = False  
      velocity = 0              
                      
     if info.menu_w.direction:  
      if (info.menu_w.x - velocity) < 900:  
      info.menu_w.move(900 - info.menu_w.x, 0)  
      else:  
      info.menu_w.move(-velocity, 0)  
      velocity += 5          
     info.menu_w.draw(screen)  
      if info.play_stop:  
      dark_screen((0, 0, 0), dark)  
      if not info.isSetting:  
      pause_w.draw(screen)  
      if dark < 150:  
      dark += 5    
                  
     if info.isSetting:    
     if info.setting_w.direction and info.isMenu:  
      if (info.setting_w.x + velocity) >= 100:  
      info.setting_w.move(100 - info.setting_w.x, 0)  
      else:  
      info.setting_w.move(velocity, 0)  
      velocity += 25    
                      
     if info.setting_w.x >= 100 and info.isMenu:  
      info.setting_w.direction = False  
      velocity = 0                        
                  
     info.setting_w.draw(screen)     
              
     if not info.play_stop and not info.isSetting and info.IsTransition:  
      dark_screen((0, 0, 0), info.dark)    
                      
     if info.isDark:  
      info.dark += 15  
      else:  
      info.dark -= 15  
      if info.dark >= 255:  
      info.isDark= False  
      start_board()  
      if info.dark <= 0:  
      info.dark = 0  
      info.isDark= True  
      info.IsTransition = False  
     if pygame.mouse.get_focused():  
      mos_pos = pygame.mouse.get_pos()  
      cur.rect.x, cur.rect.y = mos_pos  
            cursor.draw(screen)  
      
      pygame.display.flip()  
      clock.tick(fps)  
      pygame.quit()
    
И расскажу немного про работу с клетчатым полем

Функция для определения клетки на которую нажал игрок

    def get_cell_clicked(board, pos):  
      width, height = board.width * board.cell_size, board.height * board.cell_size  
        if board.left < pos[0] < board.left + width:  
      if board.top < pos[1] < board.top + height:  
      cell_coords = (pos[0] - board.left) // board.cell_size, (pos[1] - board.top) // board.cell_size  
                return cell_coords  
        return None



## Core technologies

 1. Спрайты
 2. Colide
 3. Стартовый экран
 4. Конечный экран
 5. Подсчёт результатов
 6. Анимация
 7. Несколько уровней
 8. Работа с БД


## Перевалочный пункт
- step()
1. Накачать нефть за час
Должен быть список событий.
Каждое событие включает
- Timestamp
- Сколько нефти на пункте
- Сколько добыли нефти
- Расположение
- Сколько отгрузили если надо

## Поезд
- step()
Состояния:
1. В пути
- Подвинуть вперед

2. Нагружаться нефтью
- Добавить нефти

3. Отдавать нефть
- Отдать нефть


## Cостояния поезда (define_state):
- +Если traveled_dist не равен расстоянию дороги или 0, то это  MOVING
- +Если traveled_dist равен 0 и Volume = capacity, то это MOVING (пополнились и выезжаем)
- +Если traveled_dist равен расстоянию дороги и volume равен 0, то это MOVING
- +Если traveled_dist равен 0 и volume не равен capacity и при этом в терминале есть место, то это LOADING.
        Если в терминале нет места, то это WAITING
- +Если traveled_dist равен расстоянию дороги и volume = capacity, и п.п. есть места, то это GIVEAWAY
        Если на п.п. нет места, то WAITING

## Терминалы:
(выкачивание нефти из терминала)
GIVEAWAY
- Смотрим на volume поезда, если stock >= volume то выгружаем в поезд - volume / loading_speed_train.
    Если stock <, то переходим в TAKE

TAKE
- Если stock <, то volume / generated_value и заполняем 

- Грузим нефть до тех пор, пока не появилсе в пункте поезд. (generated_value + generated_value) и так каждый час

        
## calculate_free_space
- создать список поездов и их state
- прогнать список через range
- если у поезда состояние - loading и position == Raduzney, то +1 railways в терминале Raduzney. Максимально занятых railways может быть равным из указанного числа railways
- если у поезда состояние - loading и position == Zvezda, то +1 railways в терминале Raduzney. Максимально занятых railways может быть равным из указанного числа railways
- в п.п. может быть поезда загрузки с названием trainsFinish. Эти поезда всегда будут занимать 1 место в терминале. 
Если у поезда состояние giveaway, то +1 railways, до тех пор пока не будет достигнут максимум railways

## step train

- Если состояние moving, то смотрим на speed, traveled_dist, то + speed до тех пор, пока не будет == road
- Если состояние loading, то смотрим на capacity, terminal loading и volume += terminal loading до тех пор пока == capacity и у терминала -= это кол-во
- Если состояние giveaway, то берем volume поезда и -= unloading_speed_train до тех пор пока == Volume и += это в терминал
- Если состояние waiting, смотрим на distination. Если distination - Raduzney то ждем до тех пор пока не будет free_spase, переходим затем в состояние loading. Если distination - Zvezda, то ждем до тех пор пока не будет free_spase переходим затем в состояние loading. Если distination -Polyarney, то ждем до тех пор пока не будет free_spase. Затем, если название ?= trainFinish, то переходим в состояние giweaway, else: loading
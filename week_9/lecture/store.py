from drafter import *
from bakery import assert_equal
from dataclasses import dataclass


@dataclass
class Item:
    name: str
    price: int
    stock: int


@dataclass
class State:
    items: list[Item]
    bought: list[str]
    money: int


@route
def index(state: State) -> Page:
    for_sale = []
    for item in state.items:
        if item.stock > 0:
            content = Span("Buy",
                           Button(item.name, purchase, arguments=Argument("name", item.name)),
                           "for " + str(item.price) + " coins (" + str(item.stock) + " left in stock)")
            for_sale.append(content)
    return Page(state, [
        "Welcome to the store!",
        "You have: " + str(state.money) + " coins",
        "You own: " + ", ".join(state.bought),
        "Select an item to purchase:",
        BulletedList(for_sale)
    ])


def find_item(items: list[Item], name: str) -> Item:
    for item in items:
        if item.name == name:
            return item
    return None


@route
def purchase(state: State, name: str) -> Page:
    # Is the item in the store?
    item = find_item(state.items, name)
    if item is None:
        return Page(state, [
            "Sorry, we do not have a " + name + " in stock",
            Button("Return to store", index)
        ])
    # Is the item in stock?
    elif item.stock <= 0:
        return Page(state, [
            "Sorry, we are out of stock of " + item.name,
            Button("Return to store", index)
        ])
    # Do they have enough money?
    elif state.money < item.price:
        return Page(state, [
            "You cannot afford a " + item.name,
            Button("Return to store", index)
        ])
    else:
        # Item is in stock, and player has enough money
        item.stock -= 1
        state.money -= item.price
        state.bought.append(item.name)
        return Page(state, [
            "You have purchased a " + item.name + " for " + str(item.price) + " coins",
            Button("Return to store", index)
        ])

assert_equal(
 purchase(State(items=[Item(name='Sword', price=100, stock=3), Item(name='Shield', price=50, stock=5), Item(name='Potion', price=25, stock=10)], bought=[], money=200), 'Sword'),
 Page(state=State(items=[Item(name='Sword', price=100, stock=2),
                        Item(name='Shield', price=50, stock=5),
                        Item(name='Potion', price=25, stock=10)],
                 bought=['Sword'],
                 money=100),
     content=['You have purchased a Sword for 100 coins', Button(text='Return to store', url='/')]))

assert_equal(
 index(State(items=[Item(name='Sword', price=100, stock=2), Item(name='Shield', price=50, stock=4), Item(name='Potion', price=25, stock=8)], bought=['Sword', 'Shield', 'Potion', 'Potion'], money=0)),
 Page(state=State(items=[Item(name='Sword', price=100, stock=2),
                        Item(name='Shield', price=50, stock=4),
                        Item(name='Potion', price=25, stock=8)],
                 bought=['Sword', 'Shield', 'Potion', 'Potion'],
                 money=0),
     content=['Welcome to the store!',
              'You have: 0 coins',
              'You own: Sword, Shield, Potion, Potion',
              'Select an item to purchase:',
              BulletedList(items=[Span('Buy', Button(text='Sword', url='/purchase', arguments=Argument(name='name', value='Sword')), 'for 100 coins (2 left in stock)'),
                                  Span('Buy', Button(text='Shield', url='/purchase', arguments=Argument(name='name', value='Shield')), 'for 50 coins (4 left in stock)'),
                                  Span('Buy', Button(text='Potion', url='/purchase', arguments=Argument(name='name', value='Potion')), 'for 25 coins (8 left in stock)')],
                           kind='ul')]))

assert_equal(
 index(State(items=[Item(name='Sword', price=100, stock=2), Item(name='Shield', price=50, stock=4), Item(name='Potion', price=25, stock=10)], bought=['Sword', 'Shield'], money=50)),
 Page(state=State(items=[Item(name='Sword', price=100, stock=2),
                        Item(name='Shield', price=50, stock=4),
                        Item(name='Potion', price=25, stock=10)],
                 bought=['Sword', 'Shield'],
                 money=50),
     content=['Welcome to the store!',
              'You have: 50 coins',
              'You own: Sword, Shield',
              'Select an item to purchase:',
              BulletedList(items=[Span('Buy', Button(text='Sword', url='/purchase', arguments=Argument(name='name', value='Sword')), 'for 100 coins (2 left in stock)'),
                                  Span('Buy', Button(text='Shield', url='/purchase', arguments=Argument(name='name', value='Shield')), 'for 50 coins (4 left in stock)'),
                                  Span('Buy', Button(text='Potion', url='/purchase', arguments=Argument(name='name', value='Potion')), 'for 25 coins (10 left in stock)')],
                           kind='ul')]))

assert_equal(
 index(State(items=[Item(name='Sword', price=100, stock=2), Item(name='Shield', price=50, stock=4), Item(name='Potion', price=25, stock=9)], bought=['Sword', 'Shield', 'Potion'], money=25)),
 Page(state=State(items=[Item(name='Sword', price=100, stock=2),
                        Item(name='Shield', price=50, stock=4),
                        Item(name='Potion', price=25, stock=9)],
                 bought=['Sword', 'Shield', 'Potion'],
                 money=25),
     content=['Welcome to the store!',
              'You have: 25 coins',
              'You own: Sword, Shield, Potion',
              'Select an item to purchase:',
              BulletedList(items=[Span('Buy', Button(text='Sword', url='/purchase', arguments=Argument(name='name', value='Sword')), 'for 100 coins (2 left in stock)'),
                                  Span('Buy', Button(text='Shield', url='/purchase', arguments=Argument(name='name', value='Shield')), 'for 50 coins (4 left in stock)'),
                                  Span('Buy', Button(text='Potion', url='/purchase', arguments=Argument(name='name', value='Potion')), 'for 25 coins (9 left in stock)')],
                           kind='ul')]))

assert_equal(
 purchase(State(items=[Item(name='Sword', price=100, stock=2), Item(name='Shield', price=50, stock=4), Item(name='Potion', price=25, stock=8)], bought=['Sword', 'Shield', 'Potion', 'Potion'], money=0), 'Shield'),
 Page(state=State(items=[Item(name='Sword', price=100, stock=2),
                        Item(name='Shield', price=50, stock=4),
                        Item(name='Potion', price=25, stock=8)],
                 bought=['Sword', 'Shield', 'Potion', 'Potion'],
                 money=0),
     content=['You cannot afford a Shield', Button(text='Return to store', url='/')]))

assert_equal(
 purchase(State(items=[Item(name='Sword', price=100, stock=3), Item(name='Shield', price=50, stock=5), Item(name='Potion', price=25, stock=10)], bought=[], money=200), 'Sword'),
 Page(state=State(items=[Item(name='Sword', price=100, stock=2),
                        Item(name='Shield', price=50, stock=5),
                        Item(name='Potion', price=25, stock=10)],
                 bought=['Sword'],
                 money=100),
     content=['You have purchased a Sword for 100 coins', Button(text='Return to store', url='/')]))

assert_equal(
 purchase(State(items=[Item(name='Sword', price=100, stock=2), Item(name='Shield', price=50, stock=4), Item(name='Potion', price=25, stock=9)], bought=['Sword', 'Shield', 'Potion'], money=25), 'Shield'),
 Page(state=State(items=[Item(name='Sword', price=100, stock=2),
                        Item(name='Shield', price=50, stock=4),
                        Item(name='Potion', price=25, stock=9)],
                 bought=['Sword', 'Shield', 'Potion'],
                 money=25),
     content=['You cannot afford a Shield', Button(text='Return to store', url='/')]))

assert_equal(
 purchase(State(items=[Item(name='Sword', price=100, stock=2), Item(name='Shield', price=50, stock=4), Item(name='Potion', price=25, stock=9)], bought=['Sword', 'Shield', 'Potion'], money=25), 'Sword'),
 Page(state=State(items=[Item(name='Sword', price=100, stock=2),
                        Item(name='Shield', price=50, stock=4),
                        Item(name='Potion', price=25, stock=9)],
                 bought=['Sword', 'Shield', 'Potion'],
                 money=25),
     content=['You cannot afford a Sword', Button(text='Return to store', url='/')]))

assert_equal(
 index(State(items=[Item(name='Sword', price=100, stock=2), Item(name='Shield', price=50, stock=5), Item(name='Potion', price=25, stock=10)], bought=['Sword'], money=100)),
 Page(state=State(items=[Item(name='Sword', price=100, stock=2),
                        Item(name='Shield', price=50, stock=5),
                        Item(name='Potion', price=25, stock=10)],
                 bought=['Sword'],
                 money=100),
     content=['Welcome to the store!',
              'You have: 100 coins',
              'You own: Sword',
              'Select an item to purchase:',
              BulletedList(items=[Span('Buy', Button(text='Sword', url='/purchase', arguments=Argument(name='name', value='Sword')), 'for 100 coins (2 left in stock)'),
                                  Span('Buy', Button(text='Shield', url='/purchase', arguments=Argument(name='name', value='Shield')), 'for 50 coins (5 left in stock)'),
                                  Span('Buy', Button(text='Potion', url='/purchase', arguments=Argument(name='name', value='Potion')), 'for 25 coins (10 left in stock)')],
                           kind='ul')]))

assert_equal(
 purchase(State(items=[Item(name='Sword', price=100, stock=2), Item(name='Shield', price=50, stock=4), Item(name='Potion', price=25, stock=8)], bought=['Sword', 'Shield', 'Potion', 'Potion'], money=0), 'Potion'),
 Page(state=State(items=[Item(name='Sword', price=100, stock=2),
                        Item(name='Shield', price=50, stock=4),
                        Item(name='Potion', price=25, stock=8)],
                 bought=['Sword', 'Shield', 'Potion', 'Potion'],
                 money=0),
     content=['You cannot afford a Potion', Button(text='Return to store', url='/')]))

assert_equal(
 purchase(State(items=[Item(name='Sword', price=100, stock=2), Item(name='Shield', price=50, stock=4), Item(name='Potion', price=25, stock=9)], bought=['Sword', 'Shield', 'Potion'], money=25), 'Potion'),
 Page(state=State(items=[Item(name='Sword', price=100, stock=2),
                        Item(name='Shield', price=50, stock=4),
                        Item(name='Potion', price=25, stock=8)],
                 bought=['Sword', 'Shield', 'Potion', 'Potion'],
                 money=0),
     content=['You have purchased a Potion for 25 coins', Button(text='Return to store', url='/')]))

assert_equal(
 purchase(State(items=[Item(name='Sword', price=100, stock=2), Item(name='Shield', price=50, stock=4), Item(name='Potion', price=25, stock=10)], bought=['Sword', 'Shield'], money=50), 'Potion'),
 Page(state=State(items=[Item(name='Sword', price=100, stock=2),
                        Item(name='Shield', price=50, stock=4),
                        Item(name='Potion', price=25, stock=9)],
                 bought=['Sword', 'Shield', 'Potion'],
                 money=25),
     content=['You have purchased a Potion for 25 coins', Button(text='Return to store', url='/')]))

assert_equal(
 index(State(items=[Item(name='Sword', price=100, stock=3), Item(name='Shield', price=50, stock=5), Item(name='Potion', price=25, stock=10)], bought=[], money=200)),
 Page(state=State(items=[Item(name='Sword', price=100, stock=3),
                        Item(name='Shield', price=50, stock=5),
                        Item(name='Potion', price=25, stock=10)],
                 bought=[],
                 money=200),
     content=['Welcome to the store!',
              'You have: 200 coins',
              'You own: ',
              'Select an item to purchase:',
              BulletedList(items=[Span('Buy', Button(text='Sword', url='/purchase', arguments=Argument(name='name', value='Sword')), 'for 100 coins (3 left in stock)'),
                                  Span('Buy', Button(text='Shield', url='/purchase', arguments=Argument(name='name', value='Shield')), 'for 50 coins (5 left in stock)'),
                                  Span('Buy', Button(text='Potion', url='/purchase', arguments=Argument(name='name', value='Potion')), 'for 25 coins (10 left in stock)')],
                           kind='ul')]))

assert_equal(
 purchase(State(items=[Item(name='Sword', price=100, stock=2), Item(name='Shield', price=50, stock=5), Item(name='Potion', price=25, stock=10)], bought=['Sword'], money=100), 'Shield'),
 Page(state=State(items=[Item(name='Sword', price=100, stock=2),
                        Item(name='Shield', price=50, stock=4),
                        Item(name='Potion', price=25, stock=10)],
                 bought=['Sword', 'Shield'],
                 money=50),
     content=['You have purchased a Shield for 50 coins', Button(text='Return to store', url='/')]))

assert_equal(
 purchase(State(items=[Item(name='Sword', price=100, stock=2), Item(name='Shield', price=50, stock=4), Item(name='Potion', price=25, stock=8)], bought=['Sword', 'Shield', 'Potion', 'Potion'], money=0), 'Sword'),
 Page(state=State(items=[Item(name='Sword', price=100, stock=2),
                        Item(name='Shield', price=50, stock=4),
                        Item(name='Potion', price=25, stock=8)],
                 bought=['Sword', 'Shield', 'Potion', 'Potion'],
                 money=0),
     content=['You cannot afford a Sword', Button(text='Return to store', url='/')]))

start_server(State([
    Item("Sword", 100, 3),
    Item("Shield", 50, 5),
    Item("Potion", 25, 10)
], [], 200))
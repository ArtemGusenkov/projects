from graph import graph
import sys

def main():
    if len(sys.argv) == 1:
        resp = graph.invoke({'question':'какая сегодня цена акций сбера?'})
    else:
        resp = graph.invoke({'question':f'{sys.argv[1:]}'})
    print(resp)

if __name__ == "__main__":
    main()


'''

'какая сегодня цена акций сбера?'
'что лучше всего сегодня купить на завтрак?'


'''
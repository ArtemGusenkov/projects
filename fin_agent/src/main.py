from graph import graph

def main():
    resp = graph.invoke({'question':'какая сегодня цена акций сбера?', 'history':[], 'answer':''})
    print(resp)

if __name__ == "__main__":
    main()




'''

'какая сегодня цена акций сбера?'
'что лучше всего сегодня купить на завтрак?'


'''
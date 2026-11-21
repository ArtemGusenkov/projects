from langgraph.graph import START, END, StateGraph
from states import ModMessageState
import nodes

graph_builder = StateGraph(ModMessageState)
graph_builder.add_node('classifier', nodes.question_classifier_llm)
graph_builder.add_node('ticker_finder', nodes.ticker_finder)
graph_builder.add_node('simple_stock_answer', nodes.simple_stock_answer)

graph_builder.add_edge(START, 'classifier')
graph_builder.add_conditional_edges('classifier', nodes.classifier_router, {'ticker_finder':'ticker_finder', 'END':END})
graph_builder.add_edge('ticker_finder', 'simple_stock_answer')
graph_builder.add_edge('simple_stock_answer', END)

graph = graph_builder.compile()


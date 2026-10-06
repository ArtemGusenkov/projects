from langgraph.graph import START, END, StateGraph
from states import ModMessageState
from nodes import question_classifier_llm

graph_builder = StateGraph(ModMessageState)
graph_builder.add_node('classifier', question_classifier_llm)
graph_builder.add_edge(START, 'classifier')
graph_builder.add_edge('classifier', END)

graph = graph_builder.compile()


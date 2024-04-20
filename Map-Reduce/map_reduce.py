class MapReduce:
    def __init__(self, df, sources):
        self.df = df
        self.sources = sources
        self.nodes = []

    def __distribute(self):
        list_of_nodes = []
        amount_of_nodes = len(self.sources)
        part_size = len(self.df) // amount_of_nodes
        for i in range(amount_of_nodes):
            if i == amount_of_nodes - 1:
                list_of_nodes.append(Node(self.df.iloc[i * part_size:], self.sources[i]))
            else:
                list_of_nodes.append(Node(self.df.iloc[i * part_size:(i + 1) * part_size], self.sources[i]))
        self.nodes = list_of_nodes

    def map(self):
        self.__distribute()
        for node in self.nodes:
            list_of_rows = []
            for i in range(len(node.df)):
                if any(source in node.df.iloc[i]['source'] for source in self.sources):
                    list_of_rows.append(Row(node.df.iloc[i]['source'], node.df.iloc[i]['title']))
            node.rows = list_of_rows

    def shuffle(self):
        nodes_true = []
        nodes_false = []
        for i in range(len(self.nodes)):
            node_true = Node(None, self.sources[i])
            node_false = Node(None, self.sources[i])
            nodes_true.append(node_true)
            nodes_false.append(node_false)
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes[i].rows)):
                cur_row = self.nodes[i].rows[j]
                if cur_row.source == self.nodes[i].source:
                    nodes_true[i].rows.append(cur_row)
                    continue
                else:
                    index = None
                    for k in range(len(self.sources)):
                        if cur_row.source == self.sources[k]:
                            index = k
                            break
                    nodes_false[index].rows.append(cur_row)
        nodes_lengths = []
        for i in range(len(self.nodes)):
            node_rows = nodes_true[i].rows + nodes_false[i].rows
            self.nodes[i].rows = node_rows
            nodes_lengths.append(len(self.nodes[i].rows))
        return nodes_lengths

    @staticmethod
    async def reduce(node):
        title_sum = 0
        for row in node.rows:
            title_sum += len(row.title)
        average_title_length = title_sum / len(node.rows)
        return average_title_length


class Node:
    def __init__(self, df, source):
        self.df = df
        self.source = source
        self.rows = []


class Row:
    def __init__(self, source, title):
        self.source = source
        self.title = title

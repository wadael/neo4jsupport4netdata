# -*- coding: utf-8 -*-
# Description: example netdata python.d module for monitoring Neo4j
# Author: Jerome Baton, copied from Pawel Krupa (paulfantom)


from base import SimpleService
from neo4j.v1 import GraphDatabase

# NAME = os.path.basename(__file__).replace(".chart.py", "")




class Service(SimpleService):

    update_every = 30
    priority = 9000
    retries = 1

    def __init__(self, configuration=None, name=None):
        super(self.__class__,self).__init__(configuration=configuration, name=name)

    def check(self):
        return True
    
    def create(self):
        host = self.configuration.get('host')
        boltport = self.configuration.get('boltport','7687')
        uri = "bolt://" + host + ":" + boltport

        self.neodriver = GraphDatabase.driver(uri, auth=(self.configuration.get('user'), self.configuration.get('pwd') ))

        self.chart("neo4j.neo4jmon", '', 'Monitors the total number of nodes', 'Nodes #','Nodes Count', 'line', self.priority, self.update_every)
        
        self.dimension('Total')
        return True

    def update(self, interval):
        self.begin("neo4j.neo4jmon", interval)
        
        neosession = self.neodriver.session()
        
        with neosession.begin_transaction() as tx:
            for neorecord in tx.run("MATCH (n) RETURN count(n) as nb"):
                self.set('Total', neorecord["nb"] )

        tx.close()
        neosession.close()

        self.end()
        self.commit()

        return True


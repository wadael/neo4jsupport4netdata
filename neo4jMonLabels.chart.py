# -*- coding: utf-8 -*-
# Description: example netdata python.d module for monitoring Neo4j
# Author: Jerome Baton, copied from Pawel Krupa (paulfantom)


from base import SimpleService
from neo4j.v1 import GraphDatabase

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
        self.chart("neo4j.neo4jmonlabels", '', 'Monitors the number of nodes per labels', 'Nodes #','Nodes# per Label', 'line', self.priority, self.update_every)
        
        return True

    def update(self, interval):
        self.begin("neo4j.neo4jmonlabels", interval)
        neosession = self.neodriver.session()
        
        with neosession.begin_transaction() as tx:
            for neorecord in tx.run("MATCH (a) WITH DISTINCT LABELS(a) AS temp, COUNT(a) AS tempCnt UNWIND temp AS label RETURN label, SUM(tempCnt) AS cnt ORDER BY cnt DESC LIMIT 5"):
                self.dimension( neorecord["label"] )
                self.set( neorecord["label"], neorecord["cnt"] )

        tx.close()
        neosession.close()
        self.end()
        self.commit()
        
        return True


from .LorePage import Page
import os.path
import json
from whoosh.index import create_in, open_dir
from whoosh.qparser import MultifieldParser as mfp
from whoosh.qparser import OrGroup
from whoosh.qparser import QueryParser
from whoosh.fields import *


class Searcher(object):

    def __init__(self, ixPath, dataPath=None):
        self.ix = getIX(ixPath)
        if dataPath != None:
            self.indexDB(dataPath)

    def indexDB(self, dataPath):
        writer = self.ix.writer()

        with open(dataPath, 'r') as fd:
            data = json.load(fd)

        for page in data['pages']:
            doc = getDoc(page)
            writer.add_document(
                id=str(page['id']),
                title=page['topic-name'],
                docText=doc[0],
                blurb=doc[1].split('<>')[5],
                toc=getToc(page['toc']),
                link=page['source-url'],
                img=page['img-url'],
                _stored_docText=doc[1]
            )

        # commit changes additions to whoosh database
        writer.commit()

    def testing(self):
        with self.ix.searcher() as searcher:
            tmp = list(searcher.documents())
            print(len(tmp))

    def searchID(self, pageID):
        with self.ix.searcher() as searcher:
            result = searcher.document(id=str(pageID))
            if result == None:
                return None
            return Page(result['docText'])

    def search(self, userQuery, pageNum=1, limit=10, searchType="AND"):
        resultDict = {"query": userQuery, "results": []}

        with self.ix.searcher() as searcher:
            # Conjunctive search if searchType == AND
            # Disjunctive search if searchType == OR
            # Both search types search over multiple indexed fields:
            #   title, document text, and document blurb
            if searchType == "AND":
                parser = mfp(['title', 'docText', 'blurb'],
                             schema=self.ix.schema)
            else:
                parser = mfp(['title', 'docText', 'blurb'], schema=self.ix.schema,
                             group=OrGroup)

            # parse query and search the database
            query = parser.parse(userQuery.strip())
            results = searcher.search_page(
                query, pagenum=pageNum, pagelen=limit, terms=True)

            numResults = len(results)
            # no results found, suggest a different query
            if numResults == 0:
                corrected = searcher.correct_query(query, userQuery).string
                resultDict['results'] = None
                resultDict['corrected'] = corrected
                return resultDict

            # for every result returned, append a dict object containing all
            # indexed/stored (according to schema) data to resultDict['results']
            for result in results:
                termHits = list(
                    map(lambda x: x[1].decode(), result.matched_terms()))
                resultDict['results'].append(Page(result['docText'], termHits))

            # total number of relevant docs in database
            resultDict['total-results'] = numResults
            # total pages available for search query (keeping same limit)
            resultDict['total-pages'] = numResults/limit
            # how many results were returned
            resultDict['topN'] = len(resultDict['results'])

        return resultDict


def getIX(ixPath):
    if not os.path.exists(ixPath):
        os.mkdir(ixPath)
        ix = create_in(ixPath, getSchema())
    else:
        ix = open_dir(ixPath)

    return ix


def getToc(toc):
    if toc == None or len(toc) == 0:
        return None
    else:
        return ', '.join(list(map(lambda x: x, toc)))

# returns the first paragraph found on page. Used if no blurb was found on page


def firstPara(page):
    for topic in page['toc']:
        if page[topic]['paras']:
            return page[topic]['paras']
    return ""


def getDoc(page):
    rawDoc = ""
    doc = ""

    if 'toc' not in page or page['toc'] == None:
        return None

    doc += str(page['id']) + "<>"  # page id
    doc += page['topic-name'] + "<>"  # page name
    doc += page['source-url'] + "<>"  # src url
    doc += page['img-url'] + "<>"  # image url
    doc += ','.join(page['toc']) + "<>"  # table of contents
    doc += firstPara(page) + "<>"  # blurb

    for topic in page['toc']:
        rawDoc += topic + ' '
        doc += topic + '<NAME>'
        paras = page[topic]['paras']
        lists = page[topic]['lists']

        if paras:
            doc += paras + '<PARAS>'
            rawDoc += paras + ' '
        if lists:
            for list in lists:
                for li in list:
                    doc += li + '<LI>'
                    rawDoc += li + ' '
                doc += '<LIST>'
        doc += '<TOPIC>'
    return (rawDoc, doc)


def getSchema():
    schema = Schema(
        id=ID(stored=True),
        title=TEXT(stored=True,
                   field_boost=2.0,
                   analyzer=None),
        docText=TEXT(stored=True),
        blurb=TEXT(stored=True),
        toc=STORED,
        link=STORED,
        img=STORED)

    return schema

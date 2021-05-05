
from datetime import datetime
import yaml
import aiohttp
import asyncio
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import pandas as pd
import matplotlib.pyplot as plt

async def _tick_(request):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://51.15.17.205:9000/tick/Mohamed') as response:

                json = await response.json()

                transport = AIOHTTPTransport(url="https://dbschool.alcyone.life/graphql")

                # Create a GraphQL client using the defined transport
                async with Client( transport=transport, fetch_schema_from_transport=True, ) as session:
                    for value in json['data']:
                        # Execute single query
                        query = gql(
                            """
                                mutation {
                                  createTicker(input: { data: { symbol: "%s", price: %.2f } }) {
                                    ticker {
                                      symbol
                                      price
                                    }
                                  }
                                }
                            """ % (value['symbol'], float(value['price']))
                        )

                        result = await session.execute(query)
                        print(result)
#
                return aiohttp.web.json_response(dict(json=json))
        # Select your transport with a defined url endpoint


    # $>
    except Exception as exp:
    # <!
        # !0 return what's wrong in string and the type of the exception should be enough to understand where you're wrong noobs
        return aiohttp.web.json_response({'err':{'str':str(exp),'typ':str(type(exp))}}, status=500)
#`< - - - - - - - - - - - -
async def tick_all(request):
    try:

        async with aiohttp.ClientSession() as session:
            async with session.get('http://51.15.17.205:9000/tick/Mohamed') as resp:

                info = await resp.json()
                info['timestamp'] = datetime.timestamp(datetime.now())
                data = yaml.dump(info)
                filename = f"./tick/data/{datetime.now().isoformat()}.yaml"
                with open(filename, "w") as f:
                    f.write(data)

        return aiohttp.web.json_response(info)
    except Exception as e:
        print(e)
        raise e

async def plot(request):
    try:
        async with aiohttp.ClientSession() as session:
            transport = AIOHTTPTransport(url='https://dbschool.alcyone.life/graphql')

            async with Client(transport=transport, fetch_schema_from_transport=True) as session:
                symbol = 'BTCUSDT'
                # Execute single query
                query = gql(
                    """
                        query {
                            tickers(where: { symbol_contains: "%s" }) {
                                price
                                created_at
                            }
                        }
                    """ % symbol
                )

                result = await session.execute(query)
                print(result)
                histprices = result['tickers']

                histpricesdf = pd.DataFrame.from_dict(histprices)
                # histpricesdf = histpricesdf.rename({'price': symbol}, axis=1)
                listofdf = []
                listofdf.append(histpricesdf)

                dfs = [df.set_index('created_at') for df in listofdf]
                histpriceconcat = pd.concat(dfs,axis=1)

                print(histpriceconcat)
                for i, col in enumerate(histpriceconcat.columns):
                    histpriceconcat[col].plot()
                    plt.title('Price Evolution Comparison')
                    plt.xticks(rotation=70)
                    plt.legend(histpriceconcat.columns)
                    file_path = f"./tick/plots/{symbol}.png"
                    # Saving the graph into a JPG file
                    plt.savefig(file_path, bbox_inches='tight')

            return aiohttp.web.FileResponse(f'./{file_path}')

    except Exception as exp:
        raise exp

async def plot_by_list(request):
    try:
        async with aiohttp.ClientSession() as session:
            params = request.rel_url.query['symbol'].split(',') if request.rel_url.query['symbol'] else ["BTCUSDT"]
            transport = AIOHTTPTransport(url='https://dbschool.alcyone.life/graphql')

            async with Client(transport=transport, fetch_schema_from_transport=True) as session:
                listofdf = []
                for symbol in params:
                    # Execute single query
                    query = gql(
                        """
                            query {
                                tickers(where: { symbol_contains: "%s" }) {
                                    price
                                    created_at
                                }
                            }
                        """ % symbol
                    )

                    result = await session.execute(query)
                    print(result)
                    histprices = result['tickers']

                    histpricesdf = pd.DataFrame.from_dict(histprices)
                    histpricesdf = histpricesdf.rename({'price': symbol}, axis=1)
                    listofdf.append(histpricesdf)

                dfs = [df.set_index('created_at') for df in listofdf]
                histpriceconcat = pd.concat(dfs,axis=1)

                print(histpriceconcat)
                for i, col in enumerate(histpriceconcat.columns):
                    histpriceconcat[col].plot()

                plt.title('Price Evolution Comparison')
                plt.xticks(rotation=70)
                plt.legend(histpriceconcat.columns)
                file_path = f"./tick/plots/{symbol}.png"
                # Saving the graph into a JPG file
                plt.savefig(file_path, bbox_inches='tight')

            return aiohttp.web.FileResponse(f'./{file_path}')

    except Exception as exp:
        raise exp

loop = asyncio.get_event_loop()

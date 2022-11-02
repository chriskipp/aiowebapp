
async def query(request):
    #if request.method == 'POST':
    if request.method == 'GET':
    #if True:
        response = await request.respond()
        #query = request.parameters['q']
        query = "SELECT id FROM x;"
        async with request.app.ctx.sqlite.cursor() as curs:
            await curs.execute(query)
            async for record in curs:
                await response.send(str(record))


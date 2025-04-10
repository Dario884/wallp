import pandas as pd
import plotly.express as px
import random 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import Dash,html,dcc,Input,Output
import math
import os


# FLUXO
fluxo = pd.read_excel('tabela_fluxo.xlsx')
fluxo = fluxo.drop(fluxo.shape[0]-1, axis=0) # tirando a linha de TOTAL

for c in range(0,fluxo.shape[0]):
    fluxo.loc[c,'Data']=fluxo.loc[c,'Data'][3:5]+'-'+fluxo.loc[c,'Data'][0:2]+'-'+fluxo.loc[c,'Data'][6:]
for c in range(0,fluxo.shape[0]):
    fluxo.loc[c,'Data']=pd.to_datetime(fluxo.loc[c,'Data']) # convertendo pra Datetime

for i in list(fluxo.index):
    fluxo.loc[i,'Dia']=fluxo.loc[i,'Data'].day
    fluxo.loc[i,'Mês']=fluxo.loc[i,'Data'].month
    fluxo.loc[i,'Ano']=fluxo.loc[i,'Data'].year


# ORÇAMENTO/PEDIDOS
orc = pd.read_excel('tabela_orcamento_gerada.xlsx')
# orc = orc.drop(orc.shape[0]-1, axis=0)  Não precisei porque essa tabela é do CHATGPT

for c in range(0,orc.shape[0]):
    orc.loc[c,'Data']=orc.loc[c,'Data'][3:5]+'-'+orc.loc[c,'Data'][0:2]+'-'+orc.loc[c,'Data'][6:]
for c in range(0,orc.shape[0]):
    orc.loc[c,'Data']=pd.to_datetime(orc.loc[c,'Data']) # convertendo pra Datetime
    
for i in list(orc.index):
    orc.loc[i,'Dia']=orc.loc[i,'Data'].day
    orc.loc[i,'Mês']=orc.loc[i,'Data'].month
    orc.loc[i,'Ano']=orc.loc[i,'Data'].year




# faturamento ao longo do tempo (line)
fxd = orc[['Data','Subtotal','Quantidade']].groupby('Data').sum()
fattot = fxd['Subtotal'].sum()
quanttot = fxd['Quantidade'].sum()
for i in list(fxd.index):
    fxd.loc[i,'Data']=i
fxd.rename(columns={'Subtotal':'Faturamento'}, inplace=True)
fatxdat = px.line(fxd, x='Data', y=['Faturamento','Quantidade'], color_discrete_map={'Subtotal':'darkcyan','Quantidade':'orange'},
                 markers=True, labels={'value':'Valor','variable':'Tipo de análise'}, title='Faturamento e peças vendidas ao longo do tempo')
fatxdat.update_traces(marker={'line':{'width':2,'color':'blue'}})

# personalização (DTF, SUBLIMAÇÃO, CILOGRAFIA, BORDADO) X pedidos (bar) + gastos X porcentagem (pie hole)

pergas = make_subplots(rows=3, cols=2, specs=[[{'rowspan':3,'type':'xy'}, {'rowspan':3,'type':'domain'}],
                                           [None, None],
                                           [None, None]], subplot_titles=['Personalização X Pedidos','Gastos'])
pergas.update_annotations(font_size=20)

# PERSONALIZAÇÃO
perxq = orc[['Personalização','Quantidade']].groupby('Personalização').sum()
for i in list(perxq.index):
    perxq.loc[i,'Personalização']=i
pergas.add_trace(go.Bar(x=list(perxq['Personalização']), y=list(perxq['Quantidade']), marker=dict(color=['darkblue','darkcyan','cyan','aquamarine']),
                       name='Personalizações'), row=1, col=1)
pergas.update_traces(marker={'line':{'width':2, 'color':'black'}}, row=1, col=1)
pergas.update_yaxes(title_text='Quantidade', row=1, col=1)

# GASTOS
gastos = fluxo.query('Débito > 0')
gxd = gastos[['Descrição','Débito']].groupby('Descrição').sum()
gastot = gxd['Débito'].sum()
for i in list(gxd.index):
    gxd.loc[i,'Gasto']=i
pergas.add_trace(go.Pie(labels=list(gxd['Gasto']), values=list(gxd['Débito']), marker=dict(colors=px.colors.qualitative.Alphabet), hole=0.3), row=1, col=2)
pergas.update_traces(marker={'line':{'width':2, 'color':'black'}}, row=1, col=2)

# tamanho X pedidos + tipo de roupa X pedidos + cores X pedidos (PIE)

pies = make_subplots(rows=3, cols=2, specs=[[{'rowspan':3,'type':'domain'}, {'rowspan':3,'type':'domain'}],
                                           [None, None],
                                           [None, None]], subplot_titles=['Tamanho X Pedidos','Cores X Pedidos'])
pies.update_annotations(font_size=20)

# CORES
corxq = orc[['Cor','Quantidade']].groupby('Cor').sum()
for i in list(corxq.index):
    corxq.loc[i,'Cor'] = i
x = []
y = []
cores = []
for i in list(corxq.index):
    x.append(corxq.idxmax()['Quantidade'])
    y.append(corxq.max()['Quantidade'])
    if corxq.idxmax()['Quantidade']=='AMARELO':
        cores.append('yellow')
    if corxq.idxmax()['Quantidade']=='PRETO':
        cores.append('black')
    if corxq.idxmax()['Quantidade']=='BRANCO':
        cores.append('white')
    if corxq.idxmax()['Quantidade']=='VERMELHO':
        cores.append('red')
    if corxq.idxmax()['Quantidade']=='AZUL':
        cores.append('blue')
    if corxq.idxmax()['Quantidade']=='VERDE':
        cores.append('green')
    if corxq.idxmax()['Quantidade']=='CINZA':
        cores.append('gray')
    if corxq.idxmax()['Quantidade']=='ROSA':
        cores.append('deeppink')
    if corxq.idxmax()['Quantidade']=='MARROM':
        cores.append('brown')
    if corxq.idxmax()['Quantidade']=='LARANJA':
        cores.append('orange')
    if corxq.idxmax()['Quantidade']=='ROXO':
        cores.append('purple')
    corxq = corxq.drop(corxq.idxmax()['Quantidade'], axis=0)
    
pies.add_trace(go.Pie(labels=x, values=y, marker=dict(colors=cores),pull=[0.2], hole=0.3), row=1, col=2)
pies.update_traces(marker={'line':{'width':2, 'color':'black'}}, row=1, col=2)

# TAMANHOS 
tamxq = orc[['Tamanho','Quantidade']].groupby('Tamanho').sum()
for i in list(tamxq.index):
    tamxq.loc[i,'Tamanho']=i
pies.add_trace(go.Pie(labels=list(tamxq['Tamanho']), values=list(tamxq['Quantidade']), marker=dict(colors=['darkblue','blue','darkcyan','cyan','lightcyan']),
                     pull=[0.2], hole=0.3), row=1, col=1)
pies.update_traces(marker={'line':{'width':2, 'color':'black'}}, row=1, col=1)


# ROUPA X PEDIDOS
for i in list(orc.index):
    if orc.loc[i,'Personalização'] in ['DTF','SUBLIMAÇÃO']:
        orc.loc[i,'Estampa']='Estampado'
    else:
        orc.loc[i,'Estampa']='Normal'
def estampado(prod):
    df = orc.query(f'Produto == "{prod}" and Estampa == "Estampado"')
    n = df['Quantidade'].sum()
    return n

rxq = orc[['Produto','Quantidade']].groupby('Produto').sum()
for i in list(rxq.index):
    rxq.loc[i,'Produto']=i
    rxq.loc[i,'Estampado']=estampado(rxq.loc[i,'Produto'])
    rxq.loc[i,'Normal']=rxq.loc[i,'Quantidade']-rxq.loc[i,'Estampado']
    
rxquant = px.bar(rxq, x='Produto', y=['Normal','Estampado'], title='Roupa X Pedidos', color_discrete_map={'Normal':'darkcyan','Estampado':'red'},
                labels={'variable':'Tipo','value':'Quantidade'})
rxquant.update_traces(marker={'line':{'width':2, 'color':'black'}})

















# fatxdat DARK
fatxdatdark = px.line(fxd, x='Data', y=['Faturamento','Quantidade'], color_discrete_map={'Subtotal':'darkcyan','Quantidade':'orange'},
                 markers=True, labels={'value':'Valor','variable':'Tipo de análise'}, title='Faturamento e peças vendidas ao longo do tempo',
                 template='plotly_dark')
fatxdatdark.update_traces(marker={'line':{'width':2,'color':'blue'}})

# pergas DARK

pergasdark = make_subplots(rows=3, cols=2, specs=[[{'rowspan':3,'type':'xy'}, {'rowspan':3,'type':'domain'}],
                                           [None, None],
                                           [None, None]], subplot_titles=['Personalização X Pedidos','Gastos'])
pergasdark.update_annotations(font_size=20)
pergasdark.update_layout(template='plotly_dark')

# PERSONALIZAÇÃO DARK
pergasdark.add_trace(go.Bar(x=list(perxq['Personalização']), y=list(perxq['Quantidade']), marker=dict(color=['darkblue','darkcyan','cyan','aquamarine']),
                       name='Personalizações'), row=1, col=1)
pergasdark.update_traces(marker={'line':{'width':2, 'color':'white'}}, row=1, col=1)
pergasdark.update_yaxes(title_text='Quantidade', row=1, col=1)

# GASTOS DARK
pergasdark.add_trace(go.Pie(labels=list(gxd['Gasto']), values=list(gxd['Débito']), marker=dict(colors=px.colors.qualitative.Alphabet), hole=0.3), row=1, col=2)
pergasdark.update_traces(marker={'line':{'width':2, 'color':'white'}}, row=1, col=2)

# tamanho X pedidos + tipo de roupa X pedidos + cores X pedidos (PIE) DARK

piesdark = make_subplots(rows=3, cols=2, specs=[[{'rowspan':3,'type':'domain'}, {'rowspan':3,'type':'domain'}],
                                           [None, None],
                                           [None, None]], subplot_titles=['Tamanho X Pedidos','Cores X Pedidos'])
piesdark.update_annotations(font_size=20)
piesdark.update_layout(template='plotly_dark')

# CORES DARK
piesdark.add_trace(go.Pie(labels=x, values=y, marker=dict(colors=cores),pull=[0.2], hole=0.3), row=1, col=2)
piesdark.update_traces(marker={'line':{'width':2, 'color':'white'}}, row=1, col=2)

# TAMANHOS 
piesdark.add_trace(go.Pie(labels=list(tamxq['Tamanho']), values=list(tamxq['Quantidade']), marker=dict(colors=['darkblue','blue','darkcyan','cyan','lightcyan']),
                     pull=[0.2], hole=0.3), row=1, col=1)
piesdark.update_traces(marker={'line':{'width':2, 'color':'white'}}, row=1, col=1)

# ROUPA X PEDIDOS DARK
rxquantdark = px.bar(rxq, x='Produto', y=['Normal','Estampado'], title='Roupa X Pedidos', color_discrete_map={'Normal':'darkcyan','Estampado':'red'},
                labels={'variable':'Tipo','value':'Quantidade'}, template='plotly_dark')
rxquantdark.update_traces(marker={'line':{'width':2, 'color':'white'}})



# APP
app =  Dash(__name__)
server = app.server

# INSIDE
app.layout = html.Div(children=[
    html.H1(children='ANÁLISE DE VENDAS', id='h1', style={'text-align':'center', 'font-family':'Arial', 'margin':'0px', 'padding':'5px'}),
    html.Div('Aqui estão os gráficos sobre o desempenho das vendas', id='exp',style={'text-align':'center', 'font-family':'Arial', 'margin':'0px', 'padding':'5px'}),
    dcc.Dropdown(['Claro','Escuro'], value='Claro', id = 'modo', style={'width':'50%','margin':'auto','margin-top':'30px', 'margin-bottom':'30px'}),
    html.Div(f'Faturamento total de R${fattot}', id='fat',style={'margin-left':'20px','display':'inline-block','width':'45%','font-family':'Arial', 'border-radius':'3px','margin-bottom':'20px','font-size':'2em', 'padding':'10px', 'border':'1px solid black', 'box-shadow':'-2px 2px 4px gray'}),
    html.Div(f'Peças vendidas {quanttot}', id='quant',style={'display':'inline-block','width':'45%','color':'orange','font-family':'Arial', 'border-radius':'3px','margin-bottom':'20px','margin-left':'20px','font-size':'2em', 'padding':'10px', 'border':'1px solid orange', 'box-shadow':'-2px 2px 4px gray'}),
    html.Div(f'Gasto total de R${gastot:.2f}', id='gas',style={'margin-left':'20px','display':'inline-block','width':'45%','color':'red','font-family':'Arial', 'border-radius':'3px','margin-bottom':'20px','font-size':'2em', 'padding':'10px', 'border':'1px solid red', 'box-shadow':'-2px 2px 4px gray'}),
    html.Div(f'Lucro R${fattot-gastot:.2f}', id='luc',style={'display':'inline-block','width':'45%','color':'green','font-family':'Arial', 'border-radius':'3px','margin-bottom':'20px','margin-left':'20px','font-size':'2em', 'padding':'10px', 'border':'1px solid green', 'box-shadow':'-2px 2px 4px gray'}),
    dcc.Graph(id = 'G1', figure=fatxdat),
    dcc.Graph(id = 'G2', figure=pergas),
    dcc.Graph(id = 'G3', figure=rxquant),
    dcc.Graph(id = 'G4', figure=pies),
], id='body')

# CALLBACKS
@app.callback(Output('h1','style'),
             Input('modo','value'))
def update_titulo(value):
    if value=='Escuro':
        return {'text-align':'center', 'font-family':'Arial', 'margin':'0px', 'padding':'5px','background-color':'#111111', 'color':'white'}
    if value=='Claro':
        return {'text-align':'center', 'font-family':'Arial', 'margin':'0px', 'padding':'5px'}

@app.callback(Output('exp','style'),
             Input('modo','value'))
def update_exp(value):
    if value=='Escuro':
        return {'text-align':'center', 'font-family':'Arial', 'margin':'0px', 'padding':'5px', 'background-color':'#111111', 'color':'white'}
    if value=='Claro':
        return {'text-align':'center', 'font-family':'Arial', 'margin':'0px', 'padding':'5px'}

@app.callback(Output('fat','style'),
             Input('modo','value'))
def update_fat(value):
    if value=='Escuro':
        return {'margin-left':'20px','display':'inline-block','width':'45%','font-family':'Arial', 'border-radius':'3px','margin-bottom':'20px','font-size':'2em', 'padding':'10px', 'border':'1px solid white', 'box-shadow':'-2px 2px 4px gray', 'background-color':'#111111', 'color':'white'}
    if value=='Claro':
        return {'margin-left':'20px','display':'inline-block','width':'45%','font-family':'Arial', 'border-radius':'3px','margin-bottom':'20px','font-size':'2em', 'padding':'10px', 'border':'1px solid black', 'box-shadow':'-2px 2px 4px gray'}

@app.callback(Output('quant','style'),
             Input('modo','value'))
def update_quant(value):
    if value=='Escuro':
        return {'display':'inline-block','width':'45%','color':'orange','font-family':'Arial', 'border-radius':'3px','margin-bottom':'20px','margin-left':'20px','font-size':'2em', 'padding':'10px', 'border':'1px solid orange', 'box-shadow':'-2px 2px 4px gray', 'background-color':'#111111'}
    if value=='Claro':
        return {'display':'inline-block','width':'45%','color':'orange','font-family':'Arial', 'border-radius':'3px','margin-bottom':'20px','margin-left':'20px','font-size':'2em', 'padding':'10px', 'border':'1px solid orange', 'box-shadow':'-2px 2px 4px gray'}

@app.callback(Output('gas','style'),
             Input('modo','value'))
def update_gas(value):
    if value=='Escuro':
        return {'margin-left':'20px','display':'inline-block','width':'45%','color':'red','font-family':'Arial', 'border-radius':'3px','margin-bottom':'20px','font-size':'2em', 'padding':'10px', 'border':'1px solid red', 'box-shadow':'-2px 2px 4px gray', 'background-color':'#111111'}
    if value=='Claro':
        return {'margin-left':'20px','display':'inline-block','width':'45%','color':'red','font-family':'Arial', 'border-radius':'3px','margin-bottom':'20px','font-size':'2em', 'padding':'10px', 'border':'1px solid red', 'box-shadow':'-2px 2px 4px gray'}

@app.callback(Output('luc','style'),
             Input('modo','value'))
def update_luc(value):
    if value=='Escuro':
        return {'display':'inline-block','width':'45%','color':'lightgreen','font-family':'Arial', 'border-radius':'3px','margin-bottom':'20px','margin-left':'20px','font-size':'2em', 'padding':'10px', 'border':'1px solid lightgreen', 'box-shadow':'-2px 2px 4px gray', 'background-color':'#111111'}
    if value=='Claro':
        return {'display':'inline-block','width':'45%','color':'green','font-family':'Arial', 'border-radius':'3px','margin-bottom':'20px','margin-left':'20px','font-size':'2em', 'padding':'10px', 'border':'1px solid green', 'box-shadow':'-2px 2px 4px gray'}

@app.callback(Output('body','style'),
             Input('modo','value'))
def update_body(value):
    if value=='Escuro':
        return {'background-color':'#111111'}
    if value=='Claro':
        return {'background-color':'white'}

@app.callback(Output('G1','figure'),
             Input('modo','value'))
def update_fatxdat(value):
    if value=='Escuro':
        return fatxdatdark
    if value=='Claro':
        return fatxdat

@app.callback(Output('G2','figure'),
             Input('modo','value'))
def update_pergas(value):
    if value=='Escuro':
        return pergasdark
    if value=='Claro':
        return pergas

@app.callback(Output('G3','figure'),
             Input('modo','value'))
def update_rxquant(value):
    if value=='Escuro':
        return rxquantdark
    if value=='Claro':
        return rxquant

@app.callback(Output('G4','figure'),
             Input('modo','value'))
def update_pies(value):
    if value=='Escuro':
        return piesdark
    if value=='Claro':
        return pies

# RODANDO
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050)) 
    app.run_server(debug=True, host="0.0.0.0", port=port)
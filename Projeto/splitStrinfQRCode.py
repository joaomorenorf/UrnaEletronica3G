string = "ID.9999999999,ANO.9999,TURNO.99,UF.99,MUNICIPIO.99999,ZONA ELEITORAL.9999,LOCAL VOTACAO.9999,SECAO ELEITORAL.9999|PRESIDENTE:BRANCO.0,NULO.0,LEGENDA.0,NUMERO.99999;SENADOR A:BRANCO.0,NULO.0,LEGENDA.0,NUMERO.99999;SENADOR B:BRANCO.0,NULO.0,LEGENDA.0,NUMERO.99999;DEPUTADO FEDERAL:BRANCO.0,NULO.0,LEGENDA.0,NUMERO.99999;GOVERNADOR:BRANCO.0,NULO.0,LEGENDA.0,NUMERO.99999;DEPUTADO ESTADUAL:BRANCO.0,NULO.0,LEGENDA.0,NUMERO.99999;PREFEITO:BRANCO.0,NULO.0,LEGENDA.0,NUMERO.99999;VEREADOR:BRANCO.0,NULO.0,LEGENDA.0,NUMERO.99999;PLEBISCITO:BRANCO.0,NULO.0,LEGENDA.0,NUMERO.99999"

informacoes1 = string.split("|")[0]
informacoes2 = informacoes1.split(",")
informacoes = []
for informacao in informacoes2: informacoes.append(informacao.split("."))

votos1 = string.split("|")[1]
votos2 = votos1.split(";")
votos3 = []
for cargo in votos2: votos3.append(cargo.split(":"))
votos4 = []
for voto in votos3: votos4.append([voto[0], voto[1].split(",")])
votos = []
for voto in votos4: 
	test = []
	for voto2 in voto[1]:
		test.append(voto2.split("."))
	votos.append((voto[0], test))
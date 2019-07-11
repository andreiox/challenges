import util
import functools


class Loteria:
    def __init__(self, quantidade_dezenas, total_jogos):
        if quantidade_dezenas < 6 or quantidade_dezenas > 10:
            raise Exception('Quantidade de dezenas deve ser entre 6 e 10')

        self.__quantidade_dezenas = quantidade_dezenas
        self.__total_jogos = total_jogos

    def gera_todos_jogos(self):
        self.jogos = []
        for i in range(0, self.total_jogos):
            self.jogos.append(self.__gera_dezenas())

        return self.jogos

    def realiza_sorteio(self):
        self.resultado = util.get_numeros_aleatorios_ordenados((1, 60), 6)
        return self.resultado

    def visualiza_resultado(self):
        table = []
        table.append(f'<html><head /><body>')
        table.append(f'<span>Resultado: {self.resultado}</span><br /><br />')
        table.append('<table border=1>')

        for jogo in self.jogos:
            acertos = 0
            for i in jogo:
                acertos += 1 if i in self.resultado else 0

            table.append(f'<tr><td>Jogo {jogo}</td><td>{acertos} acertos</td></tr>')

        table.append('</table></body></html>')
        return ''.join(table)

    def __gera_dezenas(self):
        return util.get_numeros_aleatorios_ordenados((1, 60), self.quantidade_dezenas)

    @property
    def total_jogos(self):
        return self.__total_jogos

    @total_jogos.setter
    def total_jogos(self, value):
        self.__total_jogos = value

    @property
    def quantidade_dezenas(self):
        return self.__quantidade_dezenas

    @quantidade_dezenas.setter
    def quantidade_dezenas(self, value):
        self.__quantidade_dezenas = value

    @property
    def jogos(self):
        return self.__jogos

    @jogos.setter
    def jogos(self, value):
        self.__jogos = value

    @property
    def resultado(self):
        return self.__resultado

    @resultado.setter
    def resultado(self, value):
        self.__resultado = value

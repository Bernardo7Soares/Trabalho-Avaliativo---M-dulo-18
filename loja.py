_saldo = 200.00

class Produto:
    listaProd = {}  # Dicionário que armazena todos os produtos disponíveis

    def __init__(self, nome, preco):
        self.num = str(len(Produto.listaProd) + 1) # Gera ID automatico
        self.nome = nome
        self.preco = float(preco)
        Produto.listaProd.update({self.num: self}) # Adiciona ao dicionario

class Carrinho:
    def __init__(self):
        self.produtos = {} # Dicionário {numero do produto: quantidade}
    
    def adicionarProd(self, num, quant): # Adiciona produto ou aumenta a quantidade se já existir
        if(num in self.produtos):
            self.produtos[num] += quant
        else:
            self.produtos[num] = quant
    
    def removerProd(self, num, quant):
        # Validações antes de remover:

        if(num not in self.produtos): # - Produto existe no carrinho
            raise ProdutoInexistenteError(num)

        if(not isStringInt(quant)):  # - Quantidade é número válido
            raise FormatoInvalidoError(quant, "int", type(quant).__name__)
                
        if(quant <= 0): # - Quantidade não é negativa/zero
            raise NumeroNegativoOuZeroError(quant)
            
        if quant > self.produtos[num]:   # - Quantidade não excede o disponível
            raise ProdutoInsuficienteError(self.produtos[num], quant)
        
        self.produtos[num] -= quant

        if(self.produtos[num] == 0):
            self.produtos.pop(num)          

    def calcularTotal(self):  # Soma o preço de todos os itens no carrinho
        total = 0
    
        for num, quant in self.produtos.items():
            total += quant * Produto.listaProd[num].preco

        return total
    
    def finalizarCompra(self):
        global _saldo

        total = self.calcularTotal()

        if(_saldo < total): # Verifica saldo suficiente
            raise SaldoInsuficienteError(_saldo, total)
        
        _saldo -= total # Subtrai total do saldo global
        self.produtos.clear()  # Limpa carrinho
        return True

# Classes de Mensagens de Erro customizadas:

class ProdutoInexistenteError(Exception): # Produto não existe
    def __init__(self, erro):
        super().__init__(f"Produto não existente: Valor: {erro}")

class OpcaoInvalidaError(Exception): # Opção inválida no menu
    def __init__(self, erro):
        super().__init__(f"Opção invalida: Valor: {erro}")

class FormatoInvalidoError(Exception): # Formato de entrada inválido
    def __init__(self, erro, formatoEsperado, formatoFornecido):
        super().__init__(f"Formato da resposta inválida, esperado '{formatoEsperado}' fornecido '{formatoFornecido}': Valor: {erro}")

class NumeroNegativoOuZeroError(Exception): # Números negativos/zero
    def __init__(self, erro):
        super().__init__(f"Números negativos ou igual a 0 não são permitidos: Valor: {erro}")

class SaldoInsuficienteError(Exception): # Saldo insuficiente
    def __init__(self, saldo, valor):
        super().__init__(f"Saldo insuficiente, valor necessário '{valor}': Saldo atual: {saldo}")

class ProdutoInsuficienteError(Exception): # Quantidade insuficiente do produto
    def __init__(self, qProd, qForn):
        super().__init__(f"Quantidade do Produto insuficiente, quantidade atual '{qProd}' quantidade desejada '{qForn}'")

class CarrinhoVazioError(Exception): # Carrinho vazio
    def __init__(self, erro):
        super().__init__(f"Carrinho Vazio: Valor: {erro}")


def preencheLista(): # Inicializa os produtos disponíveis na loja
    Produto("Secador", 25.00)
    Produto("Frigorífico", 60.50)
    Produto("Batedeira", 39.99)

def isStringInt(num): # Função auxiliar para verificar se uma string pode ser convertida em inteiro
    try:
        int(num)
        return True
    except (ValueError, TypeError):
        return False

def Loja(carrinho):
    while(True):   
        try:
            print("\nItems:")
            for num, prod in Produto.listaProd.items():
                print( num,". ", prod.nome, " ... ", prod.preco, "€")
            print("\nc. - Cancelar escolha\nv. - Voltar")

            r = input("\nEscolha o número do Produto : ").lower().strip()
            if(r in Produto.listaProd):
                while(True):
                    try:
                        q = input("\nQuantidade: ").strip()
                        if(isStringInt(q)):
                            q = int(q)
                            if(q > 0):
                                carrinho.adicionarProd(r,q)                          
                            else:
                                raise NumeroNegativoOuZeroError(q)
                        elif(q == "v"):
                            return
                        elif(q == "c"):
                            print("Seleção cancelada")
                            break
                        else:
                            raise FormatoInvalidoError(q, "int", type(q).__name__)
                    except (NumeroNegativoOuZeroError, FormatoInvalidoError) as e:
                        print(f"Erro capturado: {e}")
                    else:
                        print(f"Adicionado: {q} x {Produto.listaProd[r].nome} ao Carrinho")
                        break
            elif(r=="v"):
                return
            else:
                raise ProdutoInexistenteError(r)
        except ProdutoInexistenteError as e:
            print(f"Erro capturado: {e}")

def verCarrinho(carrinho):
    global _saldo

    while(True):
        print("\nItems no Carrinho:\n")
        if(len(carrinho.produtos)>0):
            for num, quant in carrinho.produtos.items():
                print( f"--- {num}. {quant} x {Produto.listaProd[num].nome} ... {quant * Produto.listaProd[num].preco} €")
            print(f"\nTotal: {carrinho.calcularTotal():.2f} €")
        else:
            print("Nenhum item no Carrinho...")
        print(f"\nSaldo atual: {_saldo} €")

        print("\n1.- Finalizar Compra")
        print("2.- Retirar items do Carrinho")
        print("3.- Limpar Carrinho")
        print("c.- Cancelar escolha")
        print("v.- Voltar")

        try:
            r = input("\nResposta: ").lower().strip()
            match(r):
                case "1":
                    if(len(carrinho.produtos)>0):
                        while(True):
                            try:
                                print(f"\nPreço a pagar: {carrinho.calcularTotal():.2f} €")
                                p = input("\nDeseja finalizar a Compra ?\n1.- Sim\n2.- Não\n\nResposta: ")
                                match(p):
                                    case "1": 
                                        if(carrinho.finalizarCompra()):
                                            print("\nCompra efetuada com sucesso !")
                                    case "2": print("\nCompra cancelada")
                                    case _: raise OpcaoInvalidaError(p)
                            except (OpcaoInvalidaError, SaldoInsuficienteError) as e:
                                print(f"Erro capturado: {e}")
                            else:
                                break
                    else:
                        raise CarrinhoVazioError(len(carrinho.produtos))
                case "2":
                    if(len(carrinho.produtos)>0):
                        while(True):   
                            try:
                                r = str(input("\nEscolha o número do Produto: ")).lower().strip()
                                if(r in carrinho.produtos):
                                    while(True):
                                        try:
                                            q = input("\nQuantidade: ").strip()
                                            if(isStringInt(q)):
                                                q = int(q)
                                                carrinho.removerProd(r,q)
                                            elif(q == "v"):
                                                break
                                            elif(q == "c"):
                                                print("Seleção cancelada")
                                                break
                                            else:
                                                raise FormatoInvalidoError(q, "int", type(q).__name__) 
                                        except (FormatoInvalidoError, NumeroNegativoOuZeroError, ProdutoInsuficienteError) as e:
                                            print(f"Erro capturado: {e}")
                                        else:
                                            print(f"\nRetirado: {q} x {Produto.listaProd[r].nome} ao Carrinho")
                                            break
                                    
                                    if(len(carrinho.produtos)==0):
                                        break

                                elif(r=="v"):
                                    break
                                else:
                                    raise ProdutoInexistenteError(r)
                            except ProdutoInexistenteError as e:
                                print(f"Erro capturado: {e}")
                    else:
                        raise CarrinhoVazioError(len(carrinho.produtos))
                case "3":
                    if(len(carrinho.produtos)>0):
                        carrinho.produtos.clear()
                        print("Carrinho limpo com Sucesso !")
                    else:
                        raise CarrinhoVazioError(len(carrinho.produtos))
                case "v":
                    return
                case _:
                    raise OpcaoInvalidaError(r)
        except (OpcaoInvalidaError, CarrinhoVazioError) as e:
            print(f"Erro capturado: {e}")

def Main():
    preencheLista()
    carrinho = Carrinho()
    while(True):   
        try:
            print("\n1- Produtos")
            print("2- Carrinho")
            print("3- Sair")

            r = input("\nEscolha o número: ").strip()
            match(r):
                case "1": Loja(carrinho)
                case "2": verCarrinho(carrinho)
                case "3": break
                case _: raise OpcaoInvalidaError(r)
        except OpcaoInvalidaError as e:
            print(f"Erro capturado: {e}")

Main()           
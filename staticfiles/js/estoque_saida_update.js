const currentScript = document.currentScript
const data = JSON.parse(currentScript.dataset.tokens)
const { csrf, pk } = data

const headers = { "Content-Type": "application/json", "X-CSRFToken": csrf }

const baseUrl = '/api/v1'

const getEstoque = () => ({
  items: [],
  editItem: {},
  produtos: [],
  editItem: {},

  init() {
    this.getData()
    this.getProdutos()
  },

  getData() {
    const url = `${baseUrl}/estoque-saida/${pk}`
    axios.get(url)
      .then(response => {
        this.items = response.data.map(item => {
          return { ...item, errorMessage: '' }
        })
      })
  },

  getProdutos() {
    const url = `${baseUrl}/produtos`
    axios.get(url)
      .then(response => {
        this.produtos = response.data
      })
  },

  getProduto(item) {
    // Pega a estoque atual do produto.
    const url_produto = `${baseUrl}/produtos/${item.produto}`
    axios.get(url_produto)
      .then(response => {
        item.estoque_atual = response.data.estoque
        item.saldo_atual = item.estoque_atual - item.quantidade
      })
  },

  updateItem(item) {
    // Edita o item.
    const url = `${baseUrl}/estoque-saida-item/${item.id}`

    // Remove o id, e envia o restante do item para o backend.
    // Remove também o produto porque ele está como um objeto,
    // e precisamos enviar apenas produto_id.
    const { id: _, produto: produto_nao_usado, ...bodyData } = item

    bodyData.saldo = item.produto.estoque - item.quantidade

    // Deve ser enviado o campo com o nome produto_id, pois é isso que o
    // schema do Django está esperando.
    bodyData.produto_id = produto_nao_usado.id

    item.errorMessage = ''

    axios.patch(url, bodyData, { headers })
      .then(response => console.log(response.data))
      .catch(error => item.errorMessage = error.response.data.detail)
  },

})
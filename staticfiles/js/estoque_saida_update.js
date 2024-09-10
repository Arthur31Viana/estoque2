const currentScript = document.currentScript
const data = JSON.parse(currentScript.dataset.tokens)
const { csrf, pk } = data

const headers = { "Content-Type": "application/json", "X-CSRFToken": csrf }

const baseUrl = '/api/v1'

const getEstoque = () => ({
  items: [],
  produtos: [],
  editItem: {},

  init() {
    this.getData()
    this.getProduto()
  },

  getData() {
    const url = `${baseUrl}/estoque-saida/${pk}`
    axios.get(url)
      .then(response => {
        this.items = response.data
      })
  },

  getProduto() {
    const url = `${baseUrl}/produtos`
    axios.get(url)
      .then(response => {
        this.produtos = response.data
      })
  },

  updateItem(item) {
    // Pega a estoque atual do produto.
    const url_produto = `${baseUrl}/produtos/${item.produto}`

    axios.get(url_produto)
      .then(response => {
        item.saldo = response.data.estoque - item.quantidade
      })

    // Edita o item.
    const url = `${baseUrl}/estoque-saida-item/${item.id}`

    // Remove o id, e envia o restante do item para o backend.
    const { id: _, produto: produto_id, ...bodyData } = item

    // Renomeia produto para produto_id.
    bodyData.produto_id = parseInt(produto_id)

    axios.patch(url, bodyData, { headers })
      .then(response => console.log(response.data))
  },

})
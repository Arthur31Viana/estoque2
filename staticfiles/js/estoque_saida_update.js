const currentScript = document.currentScript
const data = JSON.parse(currentScript.dataset.tokens)
const { csrf, pk } = data

const headers = { "Content-Type": "application/json", "X-CSRFToken": csrf }

const baseUrl = '/api/v1'

const getEstoque = () => ({
  items: [],
  produtos: [],
  editItem: {},
  saldo: 0,

  init() {
    this.getData()
    this.getProdutos()
  },

  getData() {
    const url = `${baseUrl}/estoque-saida/${pk}`
    axios.get(url)
      .then(response => {
        this.items = response.data
      })
  },

  getProdutos() {
    const url = `${baseUrl}/produtos`
    axios.get(url)
      .then(response => {
        this.produtos = response.data
        console.log(response.data.length)
      })
  },

  getProduto(item) {
    console.log(item.produto)
    console.table(item)
    // Pega a estoque atual do produto.
    const url_produto = `${baseUrl}/produtos/${item.produto}`
    axios.get(url_produto)
      .then(response => {
        item.saldo = response.data.estoque - item.quantidade
      })
  },

  updateItem(item) {
    // Edita o item.
    const url = `${baseUrl}/estoque-saida-item/${item.id}`

    // Remove o id, e envia o restante do item para o backend.
    const { id: _, produto: produto_id, ...bodyData } = item

    // bodyData.saldo = this.saldo

    console.log(bodyData)

    // Renomeia produto para produto_id.
    bodyData.produto_id = parseInt(produto_id)

    axios.patch(url, bodyData, { headers })
      .then(response => console.log(response.data))
  },

})
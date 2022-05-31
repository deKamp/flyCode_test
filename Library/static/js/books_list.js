
const app = Vue.createApp({
    delimiters: ["[[", "]]"],
    data() {
        return { 
            serverUrl: "http://127.0.0.1:8000",
            booksList: null,

            paginationNext: null, 
            paginationPrevious: null,
            paginationCurrentPage: null,
            paginationTotalPage: null,
            
            // Настройка когда будет показано ... (многоточие) в блоке пагинации
            pageDelta: 3,
        }
    },
    methods: {
        updateBookList(url) {
            // обновление списка книг на текущей странице. Вызывается при загрузке и смене страниц (пагинации).
            axios
                .get(url)
                .then(response => {
                    this.booksList = response.data.results

                    this.paginationTotalPage = response.data.total_pages
                    this.paginationNext = response.data.next
                    this.paginationPrevious = response.data.previous
                    this.paginationCurrentPage = response.data.pagenum
                })
                .catch(error => {
                    console.log(error)
                })
        },

        // Функции вызываемые при смене страниц (пагинации)
        setPreviosPage() {
            this.updateBookList(this.paginationPrevious)
        },
        setFirstPage() {
            this.updateBookList(this.serverUrl+"/lib/api/books/")
        },
        setNextPage() {
            this.updateBookList(this.paginationNext)
        },
        setLastPage() {
            this.updateBookList(this.serverUrl+"/lib/api/books/?page="+this.paginationTotalPage)
        }
    },

    mounted() {
        // При загрузке страницы - подгружаем список книг
        this.updateBookList(this.serverUrl+"/lib/api/books/")
    }
})


const vm = app.mount('#app')

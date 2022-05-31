
const app = Vue.createApp({
    delimiters: ["[[", "]]"],
    data() {
        return { 
            serverUrl: "http://127.0.0.1:8000",
            Comments: [],
            bookId: 0,
            addCommentText: ""
        }
    },
    methods: {
        updateComments(url) {
            // Функция обновления комментариев
            axios
                .get(url)
                .then(response => {
                    this.Comments = response.data
                })
                .catch(error => {
                    console.log(error)
                })

        },

        dateFilter(value) {
            // Приведение даты из json к приличному виду
            const d = value.split('T',1)[0].split('-')
            const t = value.split('T')[1].split(':')
            return (d[2]+"."+d[1]+"."+d[0]+" "+t[0]+":"+t[1])
        },

        addComment(){
            // Добавление комментария, очистка поля ввода.
            axios.post(this.serverUrl+"/lib/api/comments/", {"content": this.addCommentText, "book": this.bookId})
                .then((response) => {
                    this.addCommentText = ""        
                    this.updateComments(this.serverUrl+"/lib/api/comments/"+this.bookId+"/")
                })
                .catch((error) => {
                    console.log(error)
                })
        }
    },
    mounted() {
        // При загрузке страницы - получаем id книги, и обновляем список комментариев
        this.bookId = JSON.parse(document.querySelector('#book_id').textContent)
        this.updateComments(this.serverUrl+"/lib/api/comments/"+this.bookId+"/")
    }
})


const vm = app.mount('#app')

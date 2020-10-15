export default function(posts){

    const section = document.querySelector('#jssection')
    posts.forEach((post)=>{
        let container = document.createElement('article')
        container.className = 'media'
        container.className = 'content-section'
        
        let image = document.createElement('img')
        image.classList.add('rounded-circle')
        image.classList.add('article-img')
        image.src = 'static/profile_pics/'+post.author.img_file
        
        let contBody = document.createElement('div')
        let headerP = document.createElement('div')
        contBody.className = 'media-body'
        headerP.className = 'article-metadata'
        
        let a = document.createElement('a')
        a.className = 'mr-2'
        a.innerText = post.author.username
        a.href = 'user/'+post.author.username
        
        let date = document.createElement('small')
        date.className = 'text-muted'
        date.innerText = post.date_posted
        
        let title = document.createElement('h2')
        let titleA = document.createElement('a')
        titleA.className = 'article-title'
        titleA.href = 'post/'+post.id
        titleA.innerText = post.title
        let text = document.createElement('p')
        text.className = 'article-content'
        text.innerText = post.content
        headerP.appendChild(a)
        headerP.appendChild(date)

        title.appendChild(titleA)

        contBody.appendChild(headerP)
        contBody.appendChild(title)
        contBody.appendChild(text)


        container.appendChild(image)
        container.appendChild(contBody)

        section.appendChild(container)
    })

}
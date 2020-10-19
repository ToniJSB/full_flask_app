export var articuloP = Vue.component('articuloP', {
    props:['post'],
    template:`
            <article class='media content-section'>
                <img :src="'static/profile_pics/'+post.author.img_file" alt="" class="rounded-circle article-img">
                <div v-bind:class="media-body">
                    <div v-bind:class="article-metadata">
                        <a v-bind:class="mr-2" :href="users/post.author.username">{{ post.author.username }}</a>
                        <small v-bind:class="text-muted">{{ post.date_posted }}</small>
                    </div>
                    <h2><a v-bind:class="article-title" :href="post/post.id">{{ post.title }}</a></h2>
                    <p v-bind:class="article-content">{{ post.content }}</p>
                </div>
            </article>

            `
  })

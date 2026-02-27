import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ArchiveGallery from '@/views/ArchiveGallery.vue'
import ArchiveList from '@/views/ArchiveList.vue'
import AboutView from '@/views/AboutView.vue'
// import PostDetail from '@/views/PostDetail.vue' // This will be lazy-loaded

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', name: 'home', component: HomeView },
        { path: '/archive/gallery', name: 'archive-gallery', component: ArchiveGallery },
        {
            path: '/archive/list',
            name: 'archive-list',
            component: () => import('../views/ArchiveList.vue')
        },
        {
            path: '/post/:id',
            name: 'post-detail',
            component: () => import('../views/PostDetail.vue')
        },
        { path: '/about', name: 'about', component: AboutView },
    ]
})

export default router

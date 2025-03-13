<template>
  <nav class="py-5 px-8 border-b border-gray-100">
    <div class="max-w-7xl mx-auto">
      <div class="flex items-center justify-between">
        <div class="menu-left">
          <a href="#" class="text-xl">Pixelo</a>
        </div>

        <div class="menu-center flex space-x-12">
          <div class="feed-icon">
            <a href="#">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="black"
                class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z" />
              </svg>
              <h1>Feed</h1>
            </a>
          </div>

          <div class="explore-icon">
            <RouterLink :to="{ 'name': 'explore' }">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"></path>
              </svg>
              <h1>Explore</h1>
            </RouterLink>
          </div>
        </div>

        <div class="menu-right">
          <a href="#">
            <RouterLink :to="{ 'name': 'profile' }">
              <img src="./assets/charlie.jpg" class="h-15 w-15 mb-3 rounded-full object-cover">
            </RouterLink>
          </a>
        </div>
      </div>
    </div>
  </nav>

  <main class="px-8 py-8">
    <RouterView />
  </main>
</template>

<style>
.feed-icon a,
.explore-icon a {
  display: flex;
  flex-direction: row;
  gap: 8px;
}

a:hover {
  font-weight: 600;
}

main {
  background: #f5f5f5;
  min-height: 100vh;
}
</style>
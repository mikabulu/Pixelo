<template>
    <div class="grid-container">
        <div class="profile-header">
            <div class="profile-card">
                <img src="" class="profile-image">
                <p class="profile-name"><strong>User</strong></p>
                <div class="profile-stats">
                    <p class="stat">Friends</p>
                    <p class="stat">Posts</p>
                </div>
                <p class="bio">Bio</p>
            </div>
        </div>

        <div class="content-area">
            <div class="post-create">
                <div class="post-input">
                    <textarea class="input-field" placeholder="Post"></textarea>
                </div>
                <div class="post-actions">
                    <a href="#" class="btn btn-gray">Attach</a>
                    <a href="#" class="btn btn-purple">Post</a>
                </div>
            </div>

            <div class="post-card">
                <div class="post-header">
                    <div class="user-info">
                        <img src="" class="user-avatar">
                        <p class="user-name"><strong>User</strong></p>
                    </div>
                    <p class="post-time">1 minute ago</p>
                </div>
                <img src="" class="post-image">
                <div class="post-footer">
                </div>
            </div>
        </div>
    </div>
</template>

<script>

</script>
<style>
.grid-container {
    max-width: 80rem;
    margin: 0 auto;
    display: grid;
    grid-template-areas:
        "header"
        "content";
    gap: 1rem;
    width: 100%;
}

.profile-header {
    grid-area: header;
    width: 100%;
    max-width: 48rem;
    margin: 0 auto;
}

.content-area {
    grid-area: content;
    width: 100%;
    max-width: 48rem;
    margin: 0 auto;
    display: flex;
    flex-direction: row;
    gap: 1rem;
}

.post-create,
.post-card {
    width: 100%;
}

.profile-card {
    padding: 1rem;
    background-color: #bfdaa4;
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    text-align: center;
    height: 15rem;
}

.profile-image {
    margin-bottom: 1.5rem;
    border-radius: 9999px;
}

.profile-stats {
    margin-top: 1.5rem;
    display: flex;
    justify-content: space-around;
    gap: 2rem;
}

.stat {
    font-size: 0.75rem;
    color: #6b7280;
}

.bio{
    margin-top: 1.5rem;
    font-size: 0.9rem;
    background-color: white;
    padding: 2rem;
    border-radius: 0.5rem;
}

.post-create {
    background-color: white;
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
}

.post-input {
    padding: 1rem;
}

.input-field {
    width: 100%;
    padding: 1rem;
    background-color: #f3f4f6;
    border-radius: 0.5rem;
}

.post-actions {
    padding: 1rem;
    border-top: 1px solid #f3f4f6;
    display: flex;
    justify-content: space-between;
}

.btn {
    display: inline-block;
    padding: 1rem 1.5rem;
    border-radius: 0.5rem;
    color: white;
    margin: 0.5rem;
}

.btn-gray {
    background-color: #4b5563;
}

.btn-purple {
    background-color:#bfdaa4;
}

.post-card {
    padding: 1rem;
    background-color: white;
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
}

.post-header {
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.user-info {
    display: flex;
    align-items: center;
    gap: 1.5rem;
}

.user-avatar {
    width: 40px;
    border-radius: 9999px;
}

.post-time {
    color: #4b5563;
}

.post-image {
    width: 100%;
    border-radius: 0.5rem;
}

.post-footer {
    margin: 1.5rem 0;
    display: flex;
    justify-content: space-between;
}
</style>
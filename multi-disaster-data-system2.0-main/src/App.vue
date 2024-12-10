<template>
  <div id="app">
    <!-- 顶部导航栏 -->
    <header class="header">
      <h1 class="title">多元灾情数据管理系统2.0</h1>
      <div class="header-buttons">
        <button class="btn-primary" @click="goToProfile">个人中心</button>
        <button class="btn-secondary" @click="goToHome">返回首页</button>
      </div>
    </header>

    <!-- 主内容区 -->
    <div class="main-container">
      <Sidebar />
      <Content />
    </div>
  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue';
import Content from './components/Content.vue';

export default {
  name: 'App',
  components: {
    Sidebar,
    Content,
  },
  methods: {
    goToProfile() {
      alert('跳转到个人中心');
    },
    goToHome() {
      alert('返回首页');
    },
  },
};
</script>

<style>
/* 全局背景渐变 */
body {
  margin: 0;
  font-family: "Poppins", sans-serif;
  background: linear-gradient(135deg, #1e3c72, #2a5298);
  color: #ffffff;
  height: 100vh;
}

/* 顶部导航栏样式 */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(0, 0, 0, 0.5);
  padding: 20px 30px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.header .title {
  font-size: 24px;
  font-weight: bold;
  color: #ffffff;
}

.header-buttons {
  display: flex;
  gap: 15px;
}

.btn-primary {
  background: linear-gradient(90deg, #1abc9c, #16a085);
  border: none;
  padding: 10px 20px;
  border-radius: 25px;
  color: #ffffff;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-primary:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(26, 188, 156, 0.5);
}

.btn-secondary {
  background: transparent;
  border: 2px solid #1abc9c;
  color: #1abc9c;
  padding: 10px 20px;
  border-radius: 25px;
  font-weight: bold;
  cursor: pointer;
}

.btn-secondary:hover {
  background: #1abc9c;
  color: #ffffff;
}

/* 主内容区 */
.main-container {
  display: flex;
  height: calc(100vh - 80px);
  overflow: hidden;
}
</style>

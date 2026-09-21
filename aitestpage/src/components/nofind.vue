<template>
  <div>
    <el-result icon="error" title="错误提示" subTitle="404"></el-result>
    <el-button type="primary" @click="returnMain">返回主页</el-button>
  </div>
</template>

<script>
export default {
  methods: {
    returnMain () {
      this.$router.push('/')/* 跳转主页 */
    }
  }
}
</script>

<style>

</style>

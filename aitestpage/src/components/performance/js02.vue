<template>
  <div class="js-container">
    <!-- Page Header -->
    <div class="page-header">
      <h2 class="page-title">性能执行结果</h2>
      <div class="page-actions">
        <el-tag type="success">JavaScript 语法测试</el-tag>
      </div>
    </div>

    <!-- Content Card -->
    <div class="content-card">
      <!-- Data Types Section -->
      <div class="demo-section">
        <h3 class="section-title">数据类型</h3>
        <div class="button-group">
          <el-button type="primary" size="small" @click="clickButton1" icon="el-icon-document">Object 对象</el-button>
          <el-button type="primary" size="small" @click="clickButton2" icon="el-icon-s-grid">Array 数组</el-button>
          <el-button type="primary" size="small" @click="clickButton3" icon="el-icon-magic-stick">Function 函数</el-button>
        </div>
      </div>

      <!-- Operators Section -->
      <div class="demo-section">
        <h3 class="section-title">运算符</h3>
        <div class="button-group">
          <el-button type="warning" size="small" @click="clickButton4">++ 运算符</el-button>
          <el-button type="warning" size="small" @click="clickButton5">三元运算符</el-button>
        </div>
      </div>

      <!-- Control Flow Section -->
      <div class="demo-section">
        <h3 class="section-title">控制流程</h3>
        <div class="button-group">
          <el-button type="info" size="small" @click="clickButton6">Switch-Case</el-button>
          <el-button type="info" size="small" @click="clickButton7">Do-While 循环</el-button>
          <el-button type="info" size="small" @click="clickButton8">For 循环</el-button>
          <el-button type="info" size="small" @click="clickButton9">For-In 循环</el-button>
        </div>
      </div>

      <!-- Built-in Objects Section -->
      <div class="demo-section">
        <h3 class="section-title">内置对象</h3>
        <div class="button-group">
          <el-button type="success" size="small" @click="clickButton10" icon="el-icon-time">Date 日期</el-button>
          <el-button type="success" size="small" @click="clickButton11" icon="el-icon-search">RegExp 正则</el-button>
        </div>
      </div>

      <!-- Timer & Animation Section -->
      <div class="demo-section">
        <h3 class="section-title">定时器与动画</h3>
        <div class="button-group">
          <el-button type="danger" size="small" @click="clickButton12">启动定时器</el-button>
          <el-button type="danger" size="small" @click="clickButton13">停止定时器</el-button>
          <el-button type="danger" size="small" @click="clickButton14">轮播动画</el-button>
        </div>

        <!-- Animation Container -->
        <div id="view" class="animation-container">
          <ul id="img_list" class="image-list">
            <li class="image-item color-1"></li>
            <li class="image-item color-2"></li>
            <li class="image-item color-3"></li>
          </ul>
        </div>
      </div>

      <!-- Output Console -->
      <div class="console-section">
        <h3 class="section-title">
          <i class="el-icon-monitor"></i>
          执行控制台
        </h3>
        <div class="console-output">
          <p v-if="!consoleOutput.length" class="console-placeholder">点击上方按钮查看执行结果...</p>
          <div v-for="(log, index) in consoleOutput" :key="index" class="console-line">
            <span class="line-number">{{ index + 1 }}</span>
            <span class="line-content">{{ log }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    var person = {
      name: 'Bob',
      age: 20,
      tags: ['js', 'web', 'mobile'],
      city: 'Beijing',
      hasCar: true,
      zipcode: null
    }
    var list1 = [1, 2, 3, 'hello', true, null]
    var list2 = new Array([1, 2, 3, 'hello', true, null])
    var x = 10
    var y = 11
    var z = 10
    var i = 10
    var time = {
      time1: new Date(),
      time2: new Date(1517356800000),
      time3: new Date('2018/12/25 12:13:14'),
      time4: new Date(2020, 9, 12, 15, 16, 17)
    }
    var testClock
    return {
      person,
      list1,
      list2,
      x,
      y,
      z,
      i,
      value: 21,
      time,
      testClock,
      consoleOutput: []
    }
  },
  methods: {
    logToConsole (message) {
      this.consoleOutput.push(String(message))
      if (this.consoleOutput.length > 50) {
        this.consoleOutput.shift()
      }
    },
    sayHello (name) {
      return 'Hello,' + name
    },
    sayHelloByVar (name) {
      return 'Hello,' + name
    },
    clickButton1 () {
      this.logToConsole(`person.name: ${this.person.name}`)
      this.logToConsole(`person.age: ${this.person.age}`)
      this.logToConsole(`person.tags: ${JSON.stringify(this.person.tags)}`)
      this.logToConsole(`person.city: ${this.person.city}`)
      this.$message.success('Object 对象数据已输出')
    },
    clickButton2 () {
      this.logToConsole(`list1: ${JSON.stringify(this.list1)}`)
      this.logToConsole(`list2: ${JSON.stringify(this.list2)}`)
      this.$message.success('Array 数组数据已输出')
    },
    clickButton3 () {
      var res = this.sayHelloByVar('var')
      this.logToConsole(this.sayHello('not var'))
      this.logToConsole(this.sayHelloByVar(res))
      this.logToConsole(res)
      this.$message.success('Function 函数调用完成')
    },
    clickButton4 () {
      var x = 10
      var y = 10
      var z = 10
      var i = 10
      this.logToConsole(`x++ (后置++): ${x++} => x=${x}`)
      x = 11
      this.logToConsole(`x++ again: ${x++} => x=${x}`)
      this.logToConsole(`++y (前置++): ${++y} => y=${y}`)
      this.logToConsole(`z-- (后置--): ${z--} => z=${z}`)
      this.logToConsole(`--i (前置--): ${--i} => i=${i}`)
      this.$message.warning('自增/自减运算符演示')
    },
    clickButton5 () {
      const result = !(this.x > this.y)
      this.logToConsole(`${this.x} > ${this.y} ? false : true = ${result}`)
      this.$message.info('三元运算符结果: ' + result)
    },
    clickButton6 () {
      const sum = this.x + this.y
      let output = sum === this.value ? `等于${this.value}` : `不等于${this.value}`
      this.logToConsole(`${this.x} + ${this.y} = ${sum}, ${output}`)
      this.$message.info(output)
    },
    clickButton7 () {
      var sum = 0
      do {
        sum += this.x
        this.x++
      } while (this.x === 20)
      this.logToConsole(`Do-While 循环结果: sum = ${sum}`)
      this.$message.info('sum结果为' + sum)
    },
    clickButton8 () {
      let output = []
      for (var i = 1; i <= 10; i++) {
        output.push(i)
      }
      this.logToConsole(`For 循环 1-10: ${output.join(', ')}`)
      this.$message.success('For 循环执行完成')
    },
    clickButton9 () {
      let output = []
      for (var value in this.person) {
        output.push(`${value} = ${this.person[value]}`)
        this.logToConsole(`${value} = ${this.person[value]}`)
      }
      this.$message.success('For-In 遍历对象属性')
    },
    clickButton10 () {
      this.logToConsole(`当前时间: ${this.time.time1}`)
      this.logToConsole(`时间戳转换: ${this.time.time2}`)
      this.logToConsole(`字符串日期: ${this.time.time3}`)
      this.logToConsole(`参数日期: ${this.time.time4}`)
      this.$message.success('Date 对象演示')
    },
    clickButton11 () {
      var str = 'Hello World!'
      var reg = /[a-g]/g
      this.logToConsole(`reg.exec(str): ${reg.exec(str)}`)
      this.logToConsole(`reg.test(str): ${reg.test(str)}`)
      this.logToConsole(`str.search(reg): ${str.search(reg)}`)
      this.logToConsole(`str.match(reg): ${JSON.stringify(str.match(reg))}`)
      this.logToConsole(`str.replace(reg): ${str.replace(reg, '"haha"')}`)
      this.logToConsole(`str.split(reg): ${JSON.stringify(str.split(reg))}`)
      this.$message.success('正则表达式演示')
    },
    clickButton12 () {
      var num = 1
      var self = this
      var myFun = function () {
        self.logToConsole(`定时器计数: ${num++}`)
      }
      this.testClock = setInterval(myFun, 200)
      this.$message.success('定时器已启动（200ms间隔）')
    },
    clickButton13 () {
      clearInterval(this.testClock)
      this.logToConsole('定时器已停止')
      this.$message.warning('定时器已停止')
    },
    clickButton14 () {
      var imgList = document.getElementById('img_list')
      if (!imgList) return

      setInterval(function () {
        for (var i = 0; i <= 100; i++) {
          (function (pos) {
            setTimeout(function () {
              imgList.style.left = -(pos / 100) * 320 + 'px'
            }, (pos + 1) * 10)
          })(i)
        }
        var current = imgList.children[0]
        setTimeout(function () {
          imgList.appendChild(current)
          imgList.style.left = '0px'
        }, 110)
      }, 200)
      this.$message.success('轮播动画已启动')
    }
  }
}
</script>

<style scoped>
.js-container {
  padding: 24px;
  background-color: var(--bg-base);
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 20px 24px;
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
}

.page-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
}

.page-actions {
  display: flex;
  gap: 12px;
}

.content-card {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: 32px;
}

.demo-section {
  margin-bottom: 32px;
}

.demo-section:last-of-type {
  margin-bottom: 0;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 16px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.button-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

/* Animation Container */
.animation-container {
  position: relative;
  width: 320px;
  height: 120px;
  border: 2px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  overflow: hidden;
  margin-top: 16px;
  background-color: var(--bg-elevated);
}

.image-list {
  position: absolute;
  width: 960px;
  list-style: none;
  margin: 0;
  padding: 0;
  transition: left 0.1s ease;
}

.image-item {
  float: left;
  width: 320px;
  height: 120px;
}

.color-1 {
  background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
}

.color-2 {
  background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
}

.color-3 {
  background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%);
}

/* Console Output */
.console-section {
  margin-top: 32px;
  padding-top: 32px;
  border-top: 1px solid var(--border-subtle);
}

.console-output {
  background-color: var(--bg-base);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 16px;
  min-height: 200px;
  max-height: 400px;
  overflow-y: auto;
  font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
  font-size: 13px;
  line-height: 1.6;
}

.console-placeholder {
  color: var(--text-muted);
  text-align: center;
  font-style: italic;
  margin: 40px 0;
}

.console-line {
  display: flex;
  gap: 12px;
  padding: 4px 0;
  border-bottom: 1px solid rgba(63, 63, 70, 0.3);
}

.line-number {
  color: var(--text-muted);
  user-select: none;
  min-width: 30px;
  text-align: right;
}

.line-content {
  color: #22C55E;
  word-break: break-all;
}

/* Button 深色主题 */
/deep/ .el-button--default {
  background-color: var(--bg-elevated);
  border-color: var(--border-subtle);
  color: var(--text-secondary);
}

/deep/ .el-button--default:hover {
  border-color: var(--color-primary-500);
  color: var(--color-primary-500);
}

/deep/ .el-button--primary {
  background-color: var(--color-primary-500);
  border-color: var(--color-primary-500);
}

/deep/ .el-button--success {
  background-color: #22C55E;
  border-color: #22C55E;
}

/deep/ .el-button--warning {
  background-color: #F59E0B;
  border-color: #F59E0B;
}

/deep/ .el-button--danger {
  background-color: #EF4444;
  border-color: #EF4444;
}

/deep/ .el-button--info {
  background-color: var(--text-muted);
  border-color: var(--text-muted);
}

/* Tag 深色主题 */
/deep/ .el-tag--success {
  background-color: rgba(34, 197, 94, 0.15);
  border-color: #22C55E;
  color: #22C55E;
}
</style>

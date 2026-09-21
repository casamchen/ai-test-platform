const video = {
  title: {
    text: '用例执行统计'
  },
  legend: {
    // 图例文字颜色
    textStyle: {
      color: '#333'
    },
    bottom: 0
  },
  tooltip: {
    trigger: 'item'
  },
  series: [
    {
      name: '用例统计',
      type: 'pie',
      radius: '80%', // 饼图的半径
      data: [], // 这里需要填充饼图的数据
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ],
  color: [
    '#0f78f4',
    '#dd536b',
    '#9462e5',
    '#a6a6a6',
    '#e1bb22',
    '#39c362',
    '#3ed1cf'
  ]
}
export default video

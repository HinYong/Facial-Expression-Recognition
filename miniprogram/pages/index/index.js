// index.js
const app = getApp()

Page({
  data: {
    src:"/images/mrtx.png"
  },

  setPhotoInfo:function(){
    var that = this;
    wx.chooseImage(
      {
        count: 1,
        sizeType: ['original','compressed'],
        sourceType:['album','camera'],
        success: function (res){
          that.setData({
            src:res.tempFilePaths
          })
        }
      }
    )
  },

  goToCameraPage(){
    wx.navigateTo({
      url: '/pages/Camera/Camera',
    })
  },

  upload(param){
    var src=param.detail.value.imagesrc
    var that=this
    app.globalData.src=src
    console.log(app.globalData.src)
    //console.log(src)
    if(src=="/images/mrtx.png"){
      wx.showModal({
        cancelColor: 'cancelColor',
        content: '请选择图片进行上传',
        title: '提示'
      })
    }
    else{
      wx.uploadFile({
        filePath: src,
        name: 'photo',
        url: 'http://localhost:5000/emotion',
        success:function(res){
          //console.log(res.data)
          // 返回的是json格式的数据，需要转码
          var json1 = JSON.parse(res.data);
          var flag = json1['flag']
          if(flag==0){
            wx.showModal({
              cancelColor: 'cancelColor',
              content: '当前图片未检测到人脸，请重新上传！',
              title: '提示'
            })
          }
          else{
            app.globalData.angry=json1['angry']
            app.globalData.disgust=json1['disgust']
            app.globalData.happy=json1['happy']
            app.globalData.neutral=json1['neutral']
            app.globalData.fear=json1['fear']
            app.globalData.sad=json1['sad']
            app.globalData.surprise=json1['surprise']
            app.globalData.emotion=json1['emotion_text']
            wx.showToast({
              title: '上传成功！',   
              duration: 1000,
              success:function(){
                setTimeout(function(){
                  wx.navigateTo({
                    url: '/pages/Result/Result',
                  })
                },1000)
              }
            })
          }
        }
      })
    }
  },
  
  onLoad() {
    
  },
  
})

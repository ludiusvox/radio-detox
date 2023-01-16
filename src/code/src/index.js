import "./index.css";
import Vue from "vue";
import Welcome from "./components/Welcome";


let app = new Vue({
    el: '#app',
    // workaround Jinja conflict with vue
    delimiters: ['${','}'],
    methods: {

      uploadFile: function(){
 
        this.file = this.$refs.file.files[0];
 
        let formData = new FormData();
        formData.append('file', this.file);
 
        axios.post('ajaxfile.php', formData,
        {
           headers: {
             'Content-Type': 'multipart/form-data'
           }
        })
        .then(function (response) {
 
           if(!response.data){
              alert('File not uploaded.');
           }else{
              alert('File uploaded successfully.');
           }
 
        })
        .catch(function (error) {
            console.log(error);
        });
 
      }
    },
    
    
    
    
    
    components : {
        Welcome
    }

})





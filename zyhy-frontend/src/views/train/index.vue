<template>
  <div class="app-container">
    <el-row :gutter="20" type="flex" align="bottom">
      <el-col :span="16"><upload-excel-component :on-success="handleSuccess" :before-upload="beforeUpload" /></el-col>
      <el-col :span="8"> <el-button type="primary" :disabled="tableData.length == 0" @click="trainModel">Train</el-button></el-col>
    </el-row>
  
 
  <el-table :data="tableData" border highlight-current-row style="width: 100%;margin-top:20px;">
    <el-table-column v-for="item of tableHeader" :key="item" :prop="item" :label="item" />
  </el-table>

  </div>
</template>

<script>
import UploadExcelComponent from '@/components/UploadExcel/index.vue'

export default {
  name: 'Train',
  components: { UploadExcelComponent },
  data() {
    return {
     tableData: [],
      tableHeader: []
    };
  },
  methods: {
    beforeUpload(file) {
      const isLt1M = file.size / 1024 / 1024 < 1

      if (isLt1M) {
        return true
      }

      this.$message({
        message: 'Please do not upload files larger than 1m in size.',
        type: 'warning'
      })
      return false
    },
    handleSuccess({ results, header }) {
      this.tableData = results
      this.tableHeader = header
    },
    trainModel() {
      // send data to backend
      this.$message.success("开始训练...")
      const mid = -1
      window.setTimeout(() => {
        this.$router.push(`/rollback?highlightId=${mid}`)
      }, 2000);
    }
  }
}
</script>

<style scoped>
</style>





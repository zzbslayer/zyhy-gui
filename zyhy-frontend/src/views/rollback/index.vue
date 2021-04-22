<template>
  <div class="app-container">
    <el-table 
      ref="rbt" 
      v-loading="listLoading" 
      :data="list" 
      @current-change="handleCurrentChange"
      border fit highlight-current-row 
      style="width: 100%">
      <el-table-column align="center" label="ID" width="80">
        <template slot-scope="scope">
          <span>{{ scope.row.id }}</span>
        </template>
      </el-table-column>

      <el-table-column width="180px" align="center" label="日期">
        <template slot-scope="scope">
          <span>{{ scope.row.timestamp | parseTime('{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>

      <el-table-column width="120px" align="center" label="作者">
        <template slot-scope="scope">
          <span>{{ scope.row.author }}</span>
        </template>
      </el-table-column>

      <el-table-column class-name="status-col" label="状态" width="110">
        <template slot-scope="{row}">
          <el-tag :type="row.status | statusFilter">
            {{ row.status }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column min-width="300px" label="模型">
        <template slot-scope="{row}">
          <router-link :to="'/example/edit/'+row.id" class="link-type">
            <span>{{ row.title }}</span>
          </router-link>
        </template>
      </el-table-column>

      <el-table-column align="center" label="操作" width="300">
        <template slot-scope="scope">
          
          <el-button type="primary" size="small" icon="el-icon-edit" :disabled="scope.row.status !== 'done'">
            激活
          </el-button>
          &nbsp;
          <el-button type="danger" size="small">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" /> -->
  </div>
</template>

<script>
import { fetchList } from '@/api/article'
import Pagination from '@/components/Pagination' // Secondary package based on el-pagination

export default {
  name: 'Rollback',
  components: { Pagination },
  filters: {
    statusFilter(status) {
      const statusMap = {
        activated: 'success',
        done: 'info',
        training: '',
        deleted: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20
      },
      highlightId: null,
    }
  },
  mounted() {
    const highlightId = this.$route.query && this.$route.query.highlightId;
    if (highlightId) {
      this.highlightId = (Number) (highlightId);
    }

    this.getList()
      .then(list => {
        this.setCurrentRowById(this.highlightId);
      });
  },
  methods: {
    handleCurrentChange(currentRow, oldCurrentRow) {
      if (this.highlightId) {
        if (currentRow.id !== this.highlightId) {
          this.setCurrentRowById(this.highlightId);
        }
      }
    },
    setCurrentRowById(id) {
      let row;
      for (const r of this.list) {
          if (r.id == id) {
            row = r;
            break;
          }
        }
        this.setCurrent(row);
    },
    setCurrent(row) {
      this.$refs.rbt.setCurrentRow(row);
    },
    getList() {
      this.listLoading = true
      return fetchList(this.listQuery).then(response => {
        const list = response.data.items.sort((ra, rb) => {
          if (ra.status === "activated")
            return -1;
          if (rb.status === "activated")
            return 1;
          if (this.highlightId) {
            if (ra.id === this.highlightId)
              return -1;
            if (rb.id === this.highlightId)
              return 1;
          }
          return rb.timestamp - ra.timestamp;
        });
        this.list = list;
        this.total = response.data.total;
        this.listLoading = false;
        return list;
      })
    }
  }
}
</script>

<style scoped>
.edit-input {
  padding-right: 100px;
}
.cancel-btn {
  position: absolute;
  right: 15px;
  top: 10px;
}
</style>

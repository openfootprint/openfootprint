<template>
  <div>
    <b-form-file accept='.xlsx, .xls, .csv' @change="uploaded" />

    <b-modal @ok="handleOk" scrollable size="xl" ref="modal_preview" title="Please assign the columns:">

      <b-table striped hover :items="tableData.data">

        <!-- TODO https://github.com/bootstrap-vue/bootstrap-vue/issues/2737 -->
        <template :slot="'HEAD_'+field" slot-scope="data" v-for="(field, i) in tableData.header">
          {{ data.label }} <v-icon @click.native.stop="deleteColumn(field)" name="regular/times-circle" /><br/>
          <select v-model="tableData.mapping[i]">
            <option>Assign ...</option>
            <option v-for="(ck, cv) in columns" :value="cv">{{ck}}</option>
          </select>
        </template>

      </b-table>
    </b-modal>
  </div>
</template>


<script>
import XLSX from 'xlsx'
import Vue from 'vue'

export default {
  props: ["columns"],
  data () {
    return {
      rawFile: null,
      workbook: null,
      tableData: {
        header: [],
        data: [],
        mapping: []
      },
      rABS: true
    }
  },
  methods: {
    uploaded (e) {
      if (this.rawFile !== null) {
        return
      }
      this.rawFile = e.target.files[0]
      this.fileConvertToWorkbook(this.rawFile)
        .then((workbook) => {
          let xlsxArr = XLSX.utils.sheet_to_json(workbook.Sheets[workbook.SheetNames[0]])
          this.workbook = workbook
          this.tableData = this.xlsxArrToTableArr(xlsxArr);
          this.$refs.modal_preview.show()
          e.target.value = "";
          this.rawFile = null;
        })
        .catch((err) => {
          console.error(err)
        })
    },
    deleteColumn(field) {
      this.tableData.data.forEach((item) => {
        Vue.delete(item, field);
      });
    },
    handleOk() {
      var finalData = [];
      this.tableData.data.forEach((row) => {
        var mapped = {};
        this.tableData.header.forEach((col, i) => {
          if (this.tableData.mapping[i] && this.tableData.mapping[i] != "-") {
            mapped[this.tableData.mapping[i]] = row[col];
          }
        });
        finalData.push(mapped);
      });
      this.$emit("data", finalData);
    },
    fileConvertToWorkbook (file) {
      let reader = new FileReader()
      let fixdata = (data) => {
        let o = "", l = 0, w = 10240
        for( ; l<data.byteLength/w ; ++l) {
          o += String.fromCharCode.apply(null,new Uint8Array(data.slice(l*w,l*w+w)))
        }
        o += String.fromCharCode.apply(null, new Uint8Array(data.slice(l*w)))
        return o
      }
      return new Promise((resolve, reject) => {
        try {
          reader.onload = (renderEvent) => {
            let data = renderEvent.target.result
            if(this.rABS) {
              /* if binary string, read with type 'binary' */
              resolve(XLSX.read(data, {type: 'binary'}))
            } else {
              /* if array buffer, convert to base64 */
              let arr = fixdata(data)
              resolve(XLSX.read(btoa(arr), {type: 'base64'}))
            }
          }
          reader.onerror = (error) => {
            reject(error)
          }
          if (this.rABS) {
            reader.readAsBinaryString(file)
          } else {
            reader.readAsArrayBuffer(file)
          }
        } catch (error) {
          reject(error)
        }
      })
    },
    xlsxArrToTableArr (xlsxArr) {
      let tableArr = []
      let length = 0
      let maxLength = 0
      let maxLengthIndex = 0
      xlsxArr.forEach((item, index) => {
        length = Object.keys(item).length
        if (maxLength < length) {
          maxLength = length
          maxLengthIndex = index
        }
      })
      let tableHeader = Object.keys(xlsxArr[maxLengthIndex])
      let rowItem = {}
      let mapping = new Array(tableHeader.length)
      xlsxArr.forEach((item) => {
        rowItem = {}
        for (let i = 0; i < maxLength; i++) {
          rowItem[tableHeader[i]] = item[tableHeader[i]] || ''
        }
        tableArr.push(rowItem)
      })
      return {
        header: tableHeader,
        data: tableArr,
        mapping: mapping
      }
    }
  }
}
</script>
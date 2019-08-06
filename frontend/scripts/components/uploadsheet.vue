<template>
  <div>
    <label class="file-select" v-if="layout=='button'">
      <div class="select-button btn btn-border">
        <span>Select File</span>
      </div>
      <input type="file" accept='.xlsx, .xls, .csv' @change="uploaded"/>
    </label>

    <label class="file-select full_width_upload_import" v-if="layout=='full_width_upload'">
      <div class="icon_empty"><unicon name="upload"></unicon></div>
      <p>Drag and drop file here</p>
      <p>or <span>browse your files</span></p>

      <input type="file" accept='.xlsx, .xls, .csv' @change="uploaded"/>
    </label>

    <!-- <b-form-file class="toto" accept='.xlsx, .xls, .csv' @change="uploaded"/> -->

    <b-modal @ok="handleOk" scrollable size="xl" ref="modal_preview" title="Please assign the columns:">

      <b-table striped hover :items="tableData.data">

        <template :slot="'HEAD_'+field" slot-scope="data" v-for="(field, i) in tableData.header">
          {{ data.label }} <unicon name="times-circle" @click.native.stop="deleteColumn(field)"></unicon><br/>
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
  props: ["columns", "layout"],
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

<style lang="scss" scoped>
  .file-select {
    float: right;
    cursor:pointer;

    // .select-button {
    //   padding: 10px 25px;
    //   color: #000;
    //   background-color: #FFF;
    //   border:1px solid $green;
    //   border-radius: 8px;
    //   text-align: center;
    //   text-transform: uppercase;
    // }
  }

  .file-select > input[type="file"] {
    display: none;
  }
</style>
<template>
  <div>
    <label v-if="layout == 'button'" class="file-select">
      <div class="select-button btn btn-border">
        <span>Select File</span>
      </div>
      <input type="file" accept=".xlsx, .xls, .csv" @change="uploaded" />
    </label>

    <label v-if="layout == 'full_width_upload'" class="file-select full_width_upload_import">
      <div class="icon_empty"><unicon name="upload" /></div>
      <p>Drag and drop file here</p>
      <p>or <span>browse your files</span></p>

      <input type="file" accept=".xlsx, .xls, .csv" @change="uploaded" />
    </label>

    <!-- <b-form-file class="toto" accept='.xlsx, .xls, .csv' @change="uploaded"/> -->

    <b-modal
      ref="modal_preview"
      scrollable
      size="xl"
      title="Please assign the columns:"
      @ok="handleOk"
    >
      <b-table striped hover :items="tableData">
        <template
          slot="HEAD[]"
          slot-scope="data"
        >
          {{ data.label }}
          <span style="cursor:pointer;" @click.stop="deleteColumn(data.label)">(x)</span><br />
          <select v-model="mapping[data.label]">
            <option>Assign ...</option>
            <option v-for="(ck, cv) in columns" :key="ck" :value="cv">
              {{ ck }}
            </option>
          </select>
        </template>
      </b-table>
    </b-modal>
  </div>
</template>

<script>
import XLSX from "xlsx";
import Vue from "vue";

export default {
  props: ["columns", "layout"],
  data() {
    return {
      rawFile: null,
      workbook: null,
      tableData: [],
      mapping: {},
      rABS: true
    };
  },
  methods: {
    uploaded(e) {
      if (this.rawFile !== null) {
        return;
      }
      this.rawFile = e.target.files[0];
      this.fileConvertToWorkbook(this.rawFile).then(workbook => {
        let xlsxArr = XLSX.utils.sheet_to_json(workbook.Sheets[workbook.SheetNames[0]]);
        this.workbook = workbook;
        this.tableData = xlsxArr;
        this.mapping = {};
        this.$refs.modal_preview.show();
        e.target.value = "";
        this.rawFile = null;
      });
      // .catch(err => {
      //   console.error(err);
      // });
    },
    deleteColumn(field) {
      this.tableData.forEach(item => {
        Vue.delete(item, field);
      });
    },
    handleOk() {
      var finalData = [];
      this.tableData.forEach(row => {
        var mapped = {};
        Object.keys(this.mapping).forEach(k => {
          if (this.mapping[k] == "-") return;
          mapped[this.mapping[k]] = row[k];
        });
        finalData.push(mapped);
      });
      this.$emit("data", finalData);
    },
    fileConvertToWorkbook(file) {
      let reader = new FileReader();
      let fixdata = data => {
        let o = "",
          l = 0,
          w = 10240;
        for (; l < data.byteLength / w; ++l) {
          o += String.fromCharCode.apply(null, new Uint8Array(data.slice(l * w, l * w + w)));
        }
        o += String.fromCharCode.apply(null, new Uint8Array(data.slice(l * w)));
        return o;
      };
      return new Promise((resolve, reject) => {
        try {
          reader.onload = renderEvent => {
            let data = renderEvent.target.result;
            if (this.rABS) {
              /* if binary string, read with type 'binary' */
              resolve(XLSX.read(data, { type: "binary" }));
            } else {
              /* if array buffer, convert to base64 */
              let arr = fixdata(data);
              resolve(XLSX.read(btoa(arr), { type: "base64" }));
            }
          };
          reader.onerror = error => {
            reject(error);
          };
          if (this.rABS) {
            reader.readAsBinaryString(file);
          } else {
            reader.readAsArrayBuffer(file);
          }
        } catch (error) {
          reject(error);
        }
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.file-select {
  float: right;
  cursor: pointer;

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

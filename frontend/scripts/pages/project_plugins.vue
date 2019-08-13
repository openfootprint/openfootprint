<template>
  <div>
    <h2>Plugins</h2>

    <div class="row template_list">

        <article :class="{'col-lg-4':1,'template_selected': plugin.installed}" v-for="(plugin, index) in this.project.plugins">
          <b-link v-if="plugin.installed" :to="{'name':'project_plugin', 'params': {'plugin_slug': plugin.slug}}">
            <div class="template_block">
                <div class="template_preview">
                    <img src="/openfootprint/templates/reports/event1/preview.jpg" />
                </div>
                <div class="template_details">
                    <p>{{plugin.name}}</p>
                </div>
                <div class="template_selected_label"><span class="icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18.71,7.21a1,1,0,0,0-1.42,0L9.84,14.67,6.71,11.53A1,1,0,1,0,5.29,13l3.84,3.84a1,1,0,0,0,1.42,0l8.16-8.16A1,1,0,0,0,18.71,7.21Z"/></svg></span>Installed</div>

            </div>
          </b-link>

          <div v-else class="template_block">
              <div class="template_preview">
                  <img src="/openfootprint/templates/reports/event1/preview.jpg" />
              </div>
              <div class="template_details">
                  <p>{{plugin.name}}</p>
              </div>
              <b-button @click="installPlugin(index)" style="margin:10px;">Install</b-button>
          </div>

        </article>
    </div>
  </div>
</template>


<script>

export default {
  data () {
    return {
    };
  },
  mounted() {
        this.$http.post("/api/project/"+this.project.id+"/footprint").then((response) => {
        this.loading_footprint = false;
        this.total_co2e = response.data.footprint || 0;
        this.report_id = response.data.report_id;
        });
  },
  methods: {
        installPlugin: function(index) {
            this.$http.post("/api/project/"+this.project.id+"/set_plugins", [this.project.plugins[index]]).then((response) => {
                this.submitting = false;
                this.$router.push("plugins/" + this.project.plugins[index]["slug"]);
            });
        }
  },
  components: {
  }
}
</script>

<style lang="scss" scoped>
    .template_list {
        .template_block {
            border:1px solid $gray-200;
            border-radius: 8px;
            overflow: hidden;
            cursor: pointer;

            .template_preview {
                background-color:#000;
                margin-left:-15px;
                margin-right:-15px;
                min-height: 200px;

                img {
                    width:100%;
                    height:auto;
                    background-color:#000;
                }
            }

            .template_details {
                background-color:#FFF;
                padding:15px 20px;
                position: relative;

                p {
                    font-weight: bold;
                    margin:0px;
                }
            }
            &:hover .template_details .icon {
                display: block;
                &:hover {
                    svg {
                        fill:$gray-700;
                    }
                }
            }
        }

        .template_selected {
            .template_block {
                border:1px solid $green;
                position: relative;

                .template_selected_label {
                    background-color:$green;
                    color:#FFF;
                    position: absolute;
                    top:20px;
                    right:0px;
                    padding:3px 10px;
                    font-size:14px;
                    border-top-left-radius: 8px;
                    border-bottom-left-radius: 8px;

                    .icon svg {
                        width:20px;
                        margin-right:3px;
                        fill:#FFF;
                    }
                }
            }
        }
    }

</style>
<template>
    <div class="create_project_page">
        <div class="container">
            <div class="row">
                <div class="col-lg-12">
                    <a href="/"><img src="../../images/logo_openfootprint.svg" alt="Logo OpenFootprint" class="logo_create_project"/></a>
                    <!--<h1>Welcome to OpenFootprint, the footprint calculator</h1>-->
                    <div class="create_project_wrapper">
                        <h1>Create your project in 2 clicks! Select what applies:</h1>

                        <b-col lg="10" offset-lg="1">
                            <b-form class="row">
                                <span class="label col-lg-12">Project type</span>
                                <label class="col-xxs-12 col-xs-6 col-md-6 col-lg-4" id="event_project">
                                    <div :class='{"project_type": 1, "selected":kind=="event"}'>
                                        <img src="https://unicons.iconscout.com/release/v0.0.4/svg/ticket.svg" class="icon"/>
                                        <input type="radio" name="radio" value="event" v-model="kind">
                                        <span class="radiobtn"></span>
                                        <p>Event</p>
                                    </div>
                                </label>

                                <label class="col-xxs-12 col-xs-6 col-md-6 col-lg-4" id="company_project">
                                    <div :class='{"project_type": 1, "selected":kind=="company"}'>
                                        <img src="https://unicons.iconscout.com/release/v0.0.4/svg/briefcase-alt.svg" class="icon"/>
                                        <input type="radio" name="radio" value="company" v-model="kind">
                                        <span class="radiobtn"></span>
                                        <p>Company</p>
                                    </div>
                                </label>

                                <label class="col-xxs-12 col-xs-6 col-md-6 col-lg-4" id="household_project">
                                    <div :class='{"project_type": 1, "selected":kind=="household"}'>
                                        <img src="https://unicons.iconscout.com/release/v0.0.4/svg/building.svg" class="icon"/>
                                        <input type="radio" name="radio" value="household" v-model="kind">
                                        <span class="radiobtn"></span>
                                        <p>Household</p>
                                    </div>
                                </label>

                                <b-form-group class="col-lg-12">
                                    <span class="label">Project name</span>
                                    <b-input required v-model="name" placeholder="ex: OpenFootprint 2019"></b-input>
                                </b-form-group>

                                <b-button variant="success" @click="createProject()">Create {{kind}} project</b-button>
                            </b-form>
                        </b-col>
                    </div>
                </div>
            </div>
        </div>


    </div>
</template>

<script>

export default {
  data () {
    return {
      kind: "event",
      name: ""
    }
  },
  methods: {
      createProject() {
        var project = {
            "kind": this.kind,
            "name": this.name
        };
        this.$http.post("/api/project", project).then((response) => {
            //TODO catch errors
            if (response.data && response.data.id) {
                this.$router.push("project/"+response.data.id);
            }
        });
      }
  }
}
</script>

<style lang="scss" scoped>
    .create_project_page {
        padding:60px 0px;
        text-align: center;

        .logo_create_project {
            width:300px;
            margin:40px auto;
            display: block;
        }

        .create_project_wrapper {
            background-color:$gray-100;
            border-radius:10px;
            padding:40px 0px;

            h1 {
                font-size:1.5rem;
            }

            form {
                width:100%;

                .label {
                    text-align: left;
                    display: block;
                    font-size:1.125rem;
                    font-weight: bold;
                    margin-bottom:10px;
                }


                .project_type {
                    background-color: #FFF;
                    border:1px solid #E2ECFB;
                    border-radius: 10px;
                    cursor: pointer;
                    display: flex;
                    flex-direction: column;
                    height: 100%;
                    position: relative;
                    padding:60px 0px;

                    &.selected {
                        border:2px solid $green;

                        p {
                            color:$green;
                            font-weight: bold;
                        }
                    }

                    input {
                        position: absolute;
                        opacity: 0;
                        cursor: pointer;
                        height: 0;
                        width: 0;
                    }

                    .radiobtn {
                        position: absolute;
                        top: 15px;
                        right: 15px;
                        height: 25px;
                        width: 25px;
                        background-color: #FFF;
                        border: 1px solid #E2ECFB;
                        border-radius: 50%;
                    }

                    .radiobtn:after {
                        content: "";
                        position: absolute;
                        display: none;
                        left: 9px;
                        top: 5px;
                        width: 5px;
                        height: 10px;
                        border: solid #FFF;
                        border-width: 0 3px 3px 0;
                        -webkit-transform: rotate(45deg);
                        -ms-transform: rotate(45deg);
                        transform: rotate(45deg);
                    }

                    input[type="radio"]:checked ~ .radiobtn:after {
                        display: block;
                    }

                    input[type="radio"]:checked ~ .radiobtn {
                        background-color:$green;
                        border-color:$green;
                    }

                    .icon {
                        width:40px;
                        height:auto;
                        margin:0 auto 5px;
                    }

                    p {
                        margin-bottom:0px;
                    }
                }

                .form-group {
                    margin-top:30px;
                }

                button {
                    display: block;
                    margin:30px auto 0px;
                }
            }
        }
    }

</style>
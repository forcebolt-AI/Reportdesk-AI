@extends('layouts.app')

@section('content')
<div id="loader" class="lds-dual-ring hidden overlaynew"></div>
    <section class="signup-step-container">

        <div class="container">

            @if (Session::has('message'))
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    <strong>Holy guacamole!</strong> {{ Session::get('message') }}
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
            @endif
            <!-- One "tab" for each step in the form: -->
            <form class="regForm contract_form" id="regForm"action="/contract_details"method="post"
                enctype="multipart/form-data" onsubmit="return validateMyForm();">
                {{ csrf_field() }}

                <div class="tab">

                    <div class="upload-head">
                        <h1>Please Upload file</h1>
                        <p class="text-center">Please upload a signed quotation or the customer purchase order</p>
                    </div>


                    <div class="formbold-main-wrapper">
                        <!-- Author: FormBold Team -->
                        <!-- Learn More: https://formbold.com -->
                        <div class="formbold-form-wrapper">
                            <div class="mb-6">
                               

                                <div class="formbold-mb-5 formbold-file-input">
                                    <input type="file" name="file" id="file" />
                                    <label for="file">
                                        <div>
                                            <span class="formbold-drop-file text-center"> <img
                                                    src="{{ asset('asset/images/storage 1.png') }}"></span>
                                            <span class="formbold-drop-file"> Select a file or drag and drop here </span>
                                            <span class="formbold-or"> Or </span>
                                            <span class="formbold-browse"> Select file </span>
                                            <div id="up-progress">
                                                <div id="up-bar"></div>
                                                <div id="up-percent">0%</div>
                                            </div>
                                            <div id="feedback">
                                            </div>


                                        </div>
                                    </label>
                                </div>
                                <div class='alert alert-danger mt-2 d-none text-danger' id="err_file"></div>
                            </div>
                        </div>
                    </div>

                </div>
                <div class="tab">

                    <div class="upload-head">
                        <h1>Select Use Case:</h1>

                    </div>


                    <div class="formbold-main-wrapper">
                        <!-- Author: FormBold Team -->
                        <!-- Learn More: https://formbold.com -->
                        <div class="formbold-form-wrapper">
                            <div class="mb-6">
                                
                                <div class="group input-group">
                                    <select class="form-select"
                                        aria-label="Default select example "id="usecase"name="usecase">
                                        <option selected>Select Use Case</option>
                                        <option value="NewBusiness">New Business</option>
                                        <option value="Renewal">Renewal</option>
                                        <option value="Upsell">Upsell</option>

                                    </select>
                                </div>

                            </div>
                        </div>
                    </div>
                </div>
                <div class="tab">

                    <div class="upload-head">
                        <h1>Select a HubSpot Quote</h1>
                        <p class="text-center">Please select a Company, Deal,and Quotes for this contract</p>
                        <button type="button" class="btn btn-primary previewinv" data-toggle="modal" data-target="#exampleModal">
                            Open uploaded PO
                        </button>
    

                    </div>
                    <!-- Button trigger modal -->
                  
                    <!-- Modal -->
                    <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog"
                        aria-labelledby="exampleModalLabel" aria-hidden="true">
                        <div class="modal-dialog" role="document">
                            <div class="modal-content widthclass">
                              
                                    <canvas id="pdfViewer"></canvas>
                               
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                                   
                                </div>
                            </div>
                        </div>
                    </div>


                    <div class="formbold-main-wrapper newclass">
                        <!-- Author: FormBold Team -->
                        <!-- Learn More: https://formbold.com -->
                        <div class="formbold-form-wrapper contractdborder"id="newcase">
                            <div class="row impheadnew">
                                <h3 class="imphead">Contract Details:</h3>


                            </div>
                            <div class="row">
                                <div class="col-sm-3 centerclass">
                                    <label class="control-label labelcalss" for="email">Select Company</label>
                                    <div class="group input-group "id="fullwidth">
                                        <select class="form-select companydata js-example-basic-single" aria-label="Default select example"
                                            name="comapnyname" id="newbussinesscomapany">
                                            <option selected>Company</option>

                                        </select>
                                    </div>
                                    
                                </div>
                                <div class="col-sm-3 centerclass">
                                    <label class="control-label labelcalss" for="email">Select Deal</label>
                                    <div class="group input-group "id="fullwidth">
                                        <select class="form-select disable dealclass" aria-label="Default select example" name="dealname"
                                            id="dealid">
                                            <option selected>Deal</option>

                                        </select>
                                    </div>
                                    
                                </div>
                                <div class="col-sm-3 centerclass">
                                    <label class="control-label labelcalss" for="email">Select Quotes</label>
                                    <div class="group input-group "id="fullwidth">
                                        <select class="form-select disable quotesclass" aria-label="Default select example" name="quotes"
                                            id="quotes">
                                            <option selected>Quotes</option>

                                        </select>
                                    </div>
                                </div>
                                <div class="col-sm-3 centerclass" id="showhide"style="display:none">
                                    <label class="control-label labelcalss" for="email">Select Contracts</label>
                                    <div class="group input-group "id="fullwidth">
                                        <select class="form-select disable allfieldclass" aria-label="Default select example" name="contract"
                                            id="renewalcontract">
                                            <option selected>Contracts</option>

                                        </select>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="formbold-form-wrapper contractdborder">
                            <div class="bigscreen formbold-form-wrapper contractdborder">
                                <table class="table table-bordered">
                                    <thead class="bgcolord">
                                        <tr>
                                            <th id="qname">NAME</th>
                                            <th id="qsku">SKU</th>
                                            <th id="qbsd">BILLING START DATE</th>
                                            <th id="qterm">TERM(MONTHS)</th>
                                            <th id="qfreq">BILLING FREQUENCY</th>
                                            <th id="qnameqanltiyt">QUANTITY</th>
                                            <th id="qprice">UNIT PRICE</th>
                                            <th id="qdiscount">UNIT DISCOUNT</th>
                                            <th id="qnetprice">NET PRICE</th>

                                            <th id="qmrp">MRR</th>
                                            <th id="qarp">ARR</th>
                                            <th id="qtvc">TCV</th>
                                            <th id="currencyintable1">Currency</th>

                                        </tr>
                                    </thead>
                                    <tbody id="tdata">


                                    </tbody>
                                </table>

                            </div>

                            <div class="container amange_bt hideshow">
                                <label for=""style="font-size:18px !important;"><b>Total</b></label>
                                <div class="row">
                                    <div class="col-md-2">Recurring Subtotal</div>
                                    <div class="col-md-8">
                                        <hr>
                                    </div>
                                    <div class="col-md-2 recurring_total"  style="text-align: right;" id="recurring_total">$0,000/year
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-2">One-time Subtotal</div>
                                    <div class="col-md-8">
                                        <hr>
                                    </div>
                                    <div class="col-md-2 onetime_total" style="text-align: right;" id="onetime_total">$0,000</div>
                                </div>
                                <div class="row">
                                    <div class="col-md-2"><b>Subtotal</b></div>
                                    <div class="col-md-8">
                                        <hr>
                                    </div>
                                    <div class="col-md-2 sub_total" style="text-align: right;" id="sub_total"><input
                                            type="number" name="total" id="totalprice" hidden>$0,000/year</div>
                                </div>

                                <div class="row">
                                    <label for=""style="font-size:12px !important;"><b>One-time
                                            Tax*</b></label>
                                    <div class="col-md-2"><b class="taxname">GST</b></div>
                                    <div class="col-md-8">
                                        <hr>
                                    </div>
                                    <div class="col-md-2 sub_total2" style="text-align: right;"id="sub_total2">$0,000/year</div>
                                </div>
                                <div class="row">
                                    <label for=""style="font-size:12px !important;"><b>One-time
                                            Fee*</b></label>
                                    <div class="col-md-2"><b class="feename">Fee</b></div>
                                    <div class="col-md-8">
                                        <hr>
                                    </div>
                                    <div class="col-md-2 sub_total4" style="text-align: right;"id="sub_total4">$0,000/year</div>
                                </div>
                                <div class="row">
                                    <label for=""style="font-size:12px !important;"><b>One-time
                                            Discount*</b></label>
                                    <div class="col-md-2"><b class="discountname">Discount</b></div>
                                    <div class="col-md-8">
                                        <hr>
                                    </div>
                                    <div class="col-md-2 sub_total5" style="text-align: right;"id="sub_total5">$0,000/year</div>
                                </div>

                            </div>
                        </div>



                    </div>


                </div>
                <div class="tab">

                    <div class="upload-head">
                        <h1>Create Your New Workspace</h1>
                        <p class="text-center">Fill all the Workspace details</p>
                    </div>


                    <div class="formbold-main-wrapper newclass">
                        <!-- Author: FormBold Team -->
                        <!-- Learn More: https://formbold.com -->

                        <div class="formbold-form-wrapper contractdborder">
                            <div class="row impheadnew">
                                <h3 class="imphead">Workspace Details:</h3>


                            </div>
                            <div class="row">
                                <div class="col-sm-4 centerclass">
                                    <label class="control-label labelcalss" for="email">Select Workspace Type</label>
                                    <div class="group input-group">
                                        <select class="form-select" aria-label="Default select example"
                                            name="workspcetype" id="workspcetype">
                                            {{-- <option selected>Workspace Type</option> --}}
                                            <option value="Starter">Starter</option>
                                            <option  value="Creator">Creator</option>
                                            <option selected value="Trial">Trial</option>
                                            <option value="Portfolio">Portfolio</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-sm-4 centerclass">
                                    <label class="control-label labelcalss" for="email">Workspace Name</label>
                                    <div class="group input-group">
                                        <input type="text" placeholder="Workspace Name"name="workspace_name"
                                            id="workspace_name" value="">
                                    </div>
                                </div>
                                <div class="col-sm-4 centerclass">
                                    <label class="control-label labelcalss" for="email">Admin Email</label>
                                    <div class="group input-group">

                                        <select class="form-select" aria-label="Default select example" name="email"
                                            id="email">
                                            <option selected>Email</option>

                                        </select>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="formbold-form-wrapper contractdborder">
                            <div class="row impheadnew">
                                <h3 class="imphead">Invoice Details:</h3>


                            </div>
                            <div class="row">
                                <div class="col-sm-3 centerclass">
                                    <label class="control-label labelcalss" for="email">Payment Type</label>
                                    <div class="group input-group">
                                        {{-- <input type="text" placeholder="Payment Type"id="paymenttype"
                                            name="paymenttype" required> --}}
                                        <select class="form-select"
                                            aria-label="Default select example "id="paymenttype"name="paymenttype">
                                            {{-- <option selected>Payment Type</option> --}}
                                            <option value="Credit Card">Credit Card</option>
                                            <option selected value="Bank Transfer">Bank Transfer</option>

                                        </select>
                                    </div>
                                </div>
                                <div class="col-sm-3 centerclass">
                                    <label class="control-label labelcalss" for="email">Enter PO number</label>
                                    <div class="group input-group">
                                        <input type="text" placeholder="Enter PO number" id="contact_epo"
                                            name="contact_epo"/>
                                    </div>
                                </div>
                                <div class="col-sm-3 centerclass">
                                    <label class="control-label labelcalss" for="email">Select Invoice Contact</label>
                                    <div class="group input-group">
                                        {{-- <input type="text" placeholder="Invoice Contact" id="Invoice_contact"
                                            name="Invoice_contact" required> --}}
                                        <select class="form-select" aria-label="Default select example"
                                            id="Invoice_contact" name="Invoice_contact">
                                            <option selected>Invoice Contact</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-sm-3 centerclass">
                                    <label class="control-label labelcalss" for="email">Select Invoice Templates</label>
                                    <div class="group input-group">
                                        {{-- <input type="text" placeholder="Invoice Contact" id="Invoice_contact"
                                            name="Invoice_contact" required> --}}
                                        <select class="form-select" aria-label="Default select example"
                                            id="Invoice_templates" name="Invoice_templates">
                                            <option selected>Invoice Templates</option>
                                            <option value="85328c22-c5f5-49a2-afd4-c913990cd53b">International</option>
                                            <option value="0b89f4ad-bc9d-4d65-9b34-0bf9bfc31a3e">Australia</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="formbold-form-wrapper contractd">
                            <div class="row impheadnew2">
                                <h3 class="imphead">Contract Details:</h3>

                            </div>

                            <div class="row ">
                                <div class="form-group rowflexd">
                                    <label class="control-label col-sm-2" for="email">Contract Start:</label>
                                    <div class="col-sm-4">
                                        <div class="group input-group">
                                            <input type="text" placeholder="Contract Start Date"
                                                id="Contract_Start_Date" name="Contract_Start_Date"
                                                onfocus="(this.type='date')"onfocus="(this.value=new Date())">
                                        </div>
                                    </div>
                                </div>


                            </div>
                            <div class="row">
                                <div class="form-group rowflexd">
                                    <label class="control-label col-sm-2" for="email">Contract End:</label>
                                    <div class="col-sm-4 ">
                                        <div class="group input-group">
                                            <input type="text" placeholder="Contract End Date" id="Contract_end_Date"
                                                name="Contract_end_Date" onfocus="(this.type='date')">
                                        </div>
                                    </div>
                                </div>


                            </div>
                            <div class="row">


                                <div class="form-group rowflexd">
                                    <label class="control-label col-sm-2" for="email">Currency:</label>
                                    <div class="col-sm-4">
                                        <div class="group input-group">
                                            <input type="text" placeholder="Currency" id="Currency" name="Currency"
                                                readonly>
                                        </div>
                                    </div>
                                </div>

                            </div>
                            <div class="row">
                                <div class="form-group rowflexd">
                                    <label class="control-label col-sm-2" for="email">Tax:</label>
                                    <div class="col-sm-4">
                                        <div class="group input-group">
                                            <select class="form-select"
                                                aria-label="Default select example "id="GST"name="GST"
                                                readonly>
                                                <option>GST</option>
                                                <option selected value="Yes">Yes</option>
                                                <option value="No">No</option>

                                            </select>
                                        </div>
                                    </div>
                                </div>


                            </div>


                        </div>


                    </div>


                </div>
                <div class="tab">
                    <div class="upload-head">
                        <h1>Create Workspace and Invoice</h1>
                        <p class="text-center">Please check contract details and then create workspace in Django and Xero Invoice</p>
                    </div>
                    <div class="formbold-main-wrapper priview">
                        <!-- Author: FormBold Team -->
                        <!-- Learn More: https://formbold.com -->
                        <div class="formbold-form-wrapper ">
                            <div class="row gy-5 main-sdata">
                                <div class="col-sm-12 col-md-4   showdata first">
                                    <div class="form-horizontal">
                                        <div class="form-group sdata-box">
                                            <label for="a" class="col-sm-3 control-label">Contract
                                                Status:</label>
                                            <input type="text" name="contract_status" id="contract_status"
                                                class="form-control" readonly />
                                        </div>
                                        <div class="form-group sdata-box mt-2">
                                            <label for="b" class="col-sm-3 control-label">Company:</label>
                                            <textarea type="text" name="viewcomapny" id="viewcomapny"
                                                class="form-control" readonly></textarea>
                                        </div>
                                        <div class="form-group sdata-box mt-2">
                                            <label for="b" class="col-sm-3 control-label">Deal:</label>
                                            <textarea type="text" name="viewdeal" id="viewdeal" class="form-control"
                                                readonly ></textarea>
                                        </div>
                                        <div class="form-group sdata-box mt-2">
                                            <label for="b" class="col-sm-3 control-label">Quote:</label>
                                            <textarea type="text" name="viewquotes" id="viewquotes" class="form-control"
                                                readonly></textarea>
                                        </div>
                                        <div class="form-group sdata-box mt-2">
                                            <label for="b" class="col-sm-3 control-label">Contract
                                                Type:</label>
                                            <input type="text" name="contacttype" id="contacttype"
                                                class="form-control" readonly />
                                        </div>
                                    </div>



                                </div>
                                <div class="col-sm-4   showdata second">
                                    <div class="form-horizontal">
                                        <div class="form-group sdata-box">
                                            <label for="a" class="col-sm-3 control-label">Workspace
                                                Type:</label>
                                            <input type="text" name="viewworkspacetype" id="viewworkspacetype"
                                                class="form-control" readonly />
                                        </div>
                                        <div class="form-group sdata-box mt-2">
                                            <label for="b" class="col-sm-3 control-label">Org ID:</label>
                                            <input type="text" name="vieworgid" id="vieworgid" class="form-control"
                                                readonly />
                                        </div>
                                        <div class="form-group sdata-box mt-2">
                                            <label for="b" class="col-sm-3 control-label">Workspace
                                                Name:</label>
                                            <input type="text" name="viewworkspace_name" id="viewworkspace_name"
                                                class="form-control" readonly />
                                        </div>
                                        <div class="form-group sdata-box mt-2">
                                            <label for="b" class="col-sm-3 control-label">Initial
                                                Admin:</label>
                                            <input type="text" name="viewadminemail" id="viewadminemail"
                                                class="form-control" readonly />
                                        </div>

                                    </div>

                                </div>
                                <div class="col-sm-4   showdata third">
                                    <div class="form-horizontal">
                                        <div class="form-group sdata-box">
                                            <label for="a" class="col-sm-3 control-label">Creator Licence
                                                Qty:</label>
                                            <input type="number" name="creator_license_quanityt"
                                                id="creator_license_quanityt" value="999" class="form-control" readonly />
                                        </div>
                                        <div class="form-group sdata-box mt-2">
                                            <label for="b" class="col-sm-3 control-label">Viewer Licence
                                                Qty:</label>
                                            <input type="text" name="viewer_license_quanityt"
                                                id="viewer_license_quanityt" value="998" class="form-control" readonly />
                                        </div>
                                        <div class="form-group sdata-box mt-2">
                                            <label for="b" class="col-sm-3 control-label">Contract
                                                Start:</label>
                                            <input type="text" name="cstartdate" id="cstartdate" class="form-control"
                                                readonly />
                                        </div>
                                        <div class="form-group sdata-box mt-2">
                                            <label for="b" class="col-sm-3 control-label">Contract End:</label>
                                            <input type="text" name="cenddate"id="cenddate" class="form-control"
                                                readonly />
                                        </div>

                                    </div>

                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="formbold-form-wrapper contractdborder">
                        <div class="bigscreen formbold-form-wrapper contractdborder">
                            <table class="table table-bordered">
                                <thead class="bgcolord">
                                    <tr>
                                        <th id="qname">NAME</th>
                                        <th id="qsku">SKU</th>
                                        <th id="qbsd">BILLING START DATE</th>
                                        <th id="qterm">TERM(MONTHS)</th>
                                        <th id="qfreq">BILLING FREQUENCY</th>
                                        <th id="qnameqanltiyt">QUANTITY</th>
                                        <th id="qprice">UNIT PRICE</th>
                                        <th id="qdiscount">UNIT DISCOUNT</th>
                                        <th id="qnetprice">NET PRICE</th>

                                        <th id="qmrp">MRR</th>
                                        <th id="qarp">ARR</th>
                                        <th id="qtvc">TCV</th>
                                        <th id="currencyintable">Currency</th>

                                    </tr>
                                </thead>
                                <tbody id="tdata2">


                                </tbody>
                            </table>

                        </div>

                        <div class="container amange_bt hideshow">
                            <label for=""style="font-size:18px !important;"><b>Total</b></label>
                            <div class="row">
                                <div class="col-md-2">Recurring Subtotal</div>
                                <div class="col-md-8">
                                    <hr>
                                </div>
                                <div class="col-md-2 recurring_total" style="text-align: right;" id="recurring_total">$6,000/year</div>
                            </div>
                            <div class="row">
                                <div class="col-md-2">One-time Subtotal</div>
                                <div class="col-md-8">
                                    <hr>
                                </div>
                                <div class="col-md-2 onetime_total" style="text-align: right;" id="onetime_total">$4,000/year</div>
                            </div>
                            <div class="row">
                                <div class="col-md-2"><b>Subtotal</b></div>
                                <div class="col-md-8">
                                    <hr>
                                </div>
                                <div class="col-md-2 sub_total" style="text-align: right;" id="sub_total">$10,000/year</div>
                            </div>

                            <div class="row">
                                <label for=""style="font-size:12px !important;"><b>One-time
                                        Tax*</b></label>
                                <div class="col-md-2"><b class="taxname">GST</b></div>
                                <div class="col-md-8">
                                    <hr>
                                </div>
                                <div class="col-md-2 sub_total2" style="text-align: right;"id="sub_total2">0</div>
                            </div>
                            <div class="row">
                                <label for=""style="font-size:12px !important;"><b>One-time
                                        Fee*</b></label>
                                <div class="col-md-2"><b class="feename">Fee</b></div>
                                <div class="col-md-8">
                                    <hr>
                                </div>
                                <div class="col-md-2 sub_total4" style="text-align: right;"id="sub_total4">$10,000/year</div>
                            </div>
                            <div class="row">
                                <label for=""style="font-size:12px !important;"><b>One-time
                                        Discount*</b></label>
                                <div class="col-md-2"><b class="discountname">Discount</b></div>
                                <div class="col-md-8">
                                    <hr>
                                </div>
                                <div class="col-md-2 sub_total5" style="text-align: right;"id="sub_total6">$10,000/year</div>
                            </div>

                        </div>
                    </div>
                    <div class="formbold-main-wrapper priview">
                        <!-- Author: FormBold Team -->
                        <!-- Learn More: https://formbold.com -->
                        <div class="formbold-form-wrapper ">
                            <div class="row gy-5 main-sdata">
                                <div class="col-sm-12 col-md-3 mb-1 showdatanew first">
                                    <div class="form-horizontal">
                                        <div class="form-group sdata-box">
                                            <label for="a" class="col-sm-3 control-label">MRR:</label>
                                            <input type="text" name="viewmrr" id="viewmrr" class="form-control"
                                                readonly />
                                        </div>
                                        <div class="form-group sdata-box mt-2">
                                            <label for="b" class="col-sm-3 control-label">ARR:</label>
                                            <input type="text" name="viewarv" id="viewarv" class="form-control"
                                                readonly />
                                        </div>
                                        <div class="form-group sdata-box mt-2">
                                            <label for="b" class="col-sm-3 control-label">TCV:</label>
                                            <input type="text" name="viewtcv" id="viewtcv" class="form-control"
                                                readonly />
                                        </div>

                                    </div>



                                </div>
                                <div class="col-sm-4 col-md-9 mb-1 seconddiv second">
                                    <div class="row">
                                        <div class="col-sm-4 col-md-4  ">
                                            <div class="form-horizontal">
                                                <div class="form-group sdata-box">
                                                    <label for="a" class="col-sm-3 control-label">Payment
                                                        Type</label>
                                                    <input type="text" name="viewpayment" id="viewpayment"
                                                        class="form-control" readonly />
                                                </div>
                                                <div class="form-group sdata-box mt-2">
                                                    <label for="b" class="col-sm-3 control-label">Currency:</label>
                                                    <input type="text" name="viewcurrency" id="viewcurrency"
                                                        class="form-control" readonly />
                                                </div>
                                                <div class="form-group sdata-box mt-2">
                                                    <label for="b" class="col-sm-3 control-label">Tax:
                                                        Name:</label>
                                                    <input name="viewtax" type="text" id="viewtax"
                                                        class="form-control" readonly />
                                                </div>


                                            </div>
                                        </div>
                                        <div class="col-sm-4 col-md-4 mb-1">
                                            <div class="form-horizontal">
                                                <div class="form-group sdata-box">
                                                    <label for="a" class="col-sm-3 control-label">PO
                                                        Number:</label>
                                                    <input type="text" name="viewponumber" id="viewponumber"
                                                        class="form-control" readonly />
                                                </div>
                                                <div class="form-group sdata-box mt-2">
                                                    <label for="b" class="col-sm-3 control-label">Invoice
                                                        Contact:</label>
                                                    <input type="text" name="viewinvoicecontact"
                                                        id="viewinvoicecontact" class="form-control" readonly />
                                                        <input type="text" name="quotesfee"
                                                        id="quotesfee" class="form-control" hidden />
                                                        <input type="text" name="quotestax"
                                                        id="quotestax" class="form-control" hidden />
                                                        <input type="text" name="discountquotes"
                                                        id="discountquotes" class="form-control" hidden />
                                                        <input type="text" name="quotesfeename"
                                                        id="quotesfeename" class="form-control" hidden />
                                                        <input type="text" name="quotestaxname"
                                                        id="quotestaxname" class="form-control" hidden />
                                                        <input type="text" name="discountquotesname"
                                                        id="discountquotesname" class="form-control" hidden />
                                                        <input type="text" name="onetimesubtotal"
                                                        id="onetimesubtotal" class="form-control" hidden />
                                                        <input type="text" name="subtotal"
                                                        id="subtotal" class="form-control" hidden />
                                                </div>
                                                <div class="form-group sdata-box mt-2">
                                                    <label for="b" class="col-sm-3 control-label">Invoice
                                                        Template:</label>
                                                    <input type="text" name="viewinvtemp" id="viewinvtemp"
                                                        class="form-control" readonly />
                                                </div>


                                            </div>
                                        </div>
                                        <div class="col-sm-4 col-md-4 mb-1">
                                            <div class="form-horizontal">
                                                <div class="form-group sdata-box" id="xerodata">
                                                    <label for="a" class="col-sm-3 control-label">Xero Invoice
                                                        #:</label>
                                                    <input type="text" id="xerodetails" class="form-control"
                                                        readonly />
                                                </div>


                                            </div>

                                        </div>
                                    </div>

                                </div>

                            </div>
                        </div>
                    </div>
                    <div class="formbold-main-wrapper priview">
                        <!-- Author: FormBold Team -->
                        <!-- Learn More: https://formbold.com -->
                        <div class="formbold-form-wrapper ">
                            <div class="row gy-5 main-sdata">
                                <div class="col-sm-12 col-md-6 mb-1 showdatanewd first">
                                    <div class="row">
                                        <div class="col-sm-4 col-md-6  ">
                                            <div class="form-horizontal">
                                                <div class="form-group sdata-box">
                                                    <div class="create-ws"id="createWS">
                                                       
                                                        <p id="create-WS1">Create WorkSpace</p>
                                                        <p id="sucessws">WorkSpace Created Suscessfully</p>
                                                        <p id="failws">WorkSpace creations failed. Please check the details.</p>
                                                    </div>


                                                </div>



                                            </div>
                                        </div>
                                        <div class="col-sm-4 col-md-6 mb-1">
                                            <div class="form-horizontal">
                                                <div class="form-group sdata-box">
                                                    <div class="create-inv" id="create-inv">
                                                        <p id="invbutton">Create INV</p>
                                                        <p id="sucessivoice">Invoice Created Sucessfully</p>
                                                        <p id="failinvoice">Invoice creations failed. Please check the details.</p>
                                                    </div>
                                                    <div id="loader" class="lds-dual-ring hidden overlaynew"></div>
                                                    <div class="create-inv disable" id="contactid">

                                                    </div>
                                                </div>



                                            </div>
                                        </div>

                                    </div>
                                </div>

                            </div>
                        </div>
                    </div>
                </div>

            </form>
            <div class="formbold-main-wrapper">
                <!-- Author: FormBold Team -->
                <!-- Learn More: https://formbold.com -->
                <div class="formbold-form-wrapper">
                    <div style="overflow:auto;">
                        <div style="float:right;">
                            <button type="button" id="prevBtn" onclick="nextPrev(-1)">Previous</button>
                            <button type="button" id="nextBtn" onclick="nextPrev(1)">Next</button>
                        </div>
                    </div>
                </div>
            </div>

        </div>


        <!-- Circles which indicates the steps of the form: -->
        <div style="text-align:center;margin-top:40px;">
            <span class="step"></span>
            <span class="step"></span>
            <span class="step"></span>
            <span class="step"></span>
            <span class="step"></span>
        </div>

        </div>

        </div>
    </section>
@endsection

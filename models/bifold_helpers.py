from odoo.exceptions import UserError
import logging
import math
def create_cortizo(length,height,left,right,opening,sill_type,jamb_type,slide_type,point_lock,LTH):
    logger = logging.getLogger("Bifold Logger: ")
    width_deduction=[]
    num_end=0
    left_pair=0
    right_pair=0
    right_swing=0
    left_swing=0
    bool_roller=0
    one_side_pair=0
    def possibility(La,Ha):
        if((600<La<1200)and(1900<Ha<3000)):
            return 1
        return 0


    #shutter width and shutter height are the main variables which depend on the options like sill_type, jamb_type etc
    #depending on that options width and height are deducted to obtain shutter height and width
    if(left==0 or right==0):
        num_end=1
        if((left+right)%2==0):
            one_side_pair=int((left+right)/2)
            one_side_swing=(left+right)%2
            if(slide_type=="H/Roller"):
                bool_roller=1
            else:
                bool_roller=0
        else:
            Wall_swing=1
    else:
        num_end=2
        left_pair=int(left/2)
        right_pair=int(right/2)
        left_swing=left%2
        right_swing=right%2
        if(slide_type=="H/Roller"):
            bool_roller=1
        else:
            bool_roller=0

    if(jamb_type=='ADJ'):
        width_deduction.append(2*(35+21.5))
    else:
        width_deduction.append(2*35)
    
    width_deduction.append((right+left)*10)
    if(num_end>1):
        if(left_swing+right_swing==2):
            width_deduction.append(29)
        elif(left_swing+right_swing==0):
            if(bool_roller):
                width_deduction.append(45)
            else:
                width_deduction.append(85)
        else:
            if(bool_roller):
                width_deduction.append(30)
            else:
                width_deduction.append(56)
    else:
        if(one_side_swing==1):
            width_deduction.append(21)
        else:
            if(bool_roller):
                width_deduction.append(33)
            else:
                width_deduction.append(48)
    height_deduction=[]

    if(LTH=='Recess'):
        if(sill_type=='LTH-1'):
            height_deduction.append(-16)
        elif(sill_type=='LTH-2'):
            height_deduction.append(-22)
    if(sill_type=='STD'):
        height_deduction.append(115)
    elif(sill_type=='LTH-1'):
        height_deduction.append(100)
    else:
        height_deduction.append(106)
    print(width_deduction)
    print(sum(width_deduction)) 
    print(height_deduction)
    print(sum(height_deduction))
    shutter_width=(length-sum(width_deduction))/(left+right)
    shutter_height=height-sum(height_deduction)
    print(shutter_width)
    print(shutter_height)


    if(possibility(shutter_width,shutter_height)):

        componentlist=[]
        L=0
        if(sill_type=="STD"):
            shape="45-45"
            L=height
        elif(sill_type=="LTH-1"):
            shape="45-90"
            if(LTH=="Recess"):
                L=height-20+16
            else:
                L=height-20
        elif(sill_type=="LTH-2"):
            shape="45-90"
            if(LTH=="Recess"):
                L=height-26+22
            else:
                L=height-26  
        if(length>2000):  
            componentlist.append(["COR-3731","Lateral Frame",shape,L,2])
            componentlist.append(["COR-3731","Lateral Frame","45-45",length,1])
        if(sill_type=="STD"):
            shape="45-45"
            L=length
            units=1
            componentlist.append(["COR-3730","Cill Frame with inox rail",shape,L,units])
        componentlist.append(["COR-3721","55mm Slim Sash","45-45",shutter_width,2*(left+right)])
        componentlist.append(["COR-3721","55mm Slim Sash","45-45",shutter_height,2*(left+right)])

        MDL_D_swing=0
        MDL_SP_SP=0
        MDL_HR_HR=0
        MDL_P_swing=0
        MDL_H_swing=0
        Wall_swing=0
        Wall_SP_lock=0
        Wall_HR_lock=0
   #     B_wall=0
        # B_middle=0
        if(left==0 or right==0):
            if((left+right)%2==0):
                if(slide_type=="H/Roller"):
                    Wall_HR_lock=1
                elif(slide_type=="Post"):
                    Wall_SP_lock=1
            else:
                Wall_swing=1
        else:
            if(left%2==0 and right%2==0):
                if(slide_type=="H/Roller"):
                    MDL_HR_HR=1
                elif(slide_type=="Post"):
                    MDL_SP_SP=1
            elif(left%2==1 and right%2==1):
                MDL_D_swing=1
            else:
                if(slide_type=="H/Roller"):
                    MDL_H_swing=1
                elif(slide_type=="Post"):
                    MDL_P_swing=1

        
        print(Wall_swing,Wall_SP_lock,Wall_HR_lock,MDL_D_swing,MDL_P_swing,MDL_H_swing,MDL_SP_SP,MDL_HR_HR)
        units=(left+right-Wall_swing-MDL_P_swing-2*MDL_H_swing-2*MDL_D_swing-2*MDL_HR_HR)*2

        componentlist.append(["COR-3725","Sash Extension","90-90",shutter_width,units])
        if(Wall_swing+MDL_H_swing+MDL_P_swing==1):
            units= 2
            L=shutter_width+8
            componentlist.append(["COR-3725","Sash Extension","90-90",L,units])
        elif(MDL_D_swing==1):
            L=shutter_width+8
            units=4
            componentlist.append(["COR-3725","Sash Extension","90-90",L,units])
        if(Wall_HR_lock+MDL_H_swing==1):
            units= 2
            L=shutter_width+9
            componentlist.append(["COR-3725","Sash Extension","90-90",L,units])
        elif(MDL_HR_HR==1):
            L=shutter_width+9
            units=4
            componentlist.append(["COR-3725","Sash Extension","90-90",L,units])

        if(Wall_SP_lock+MDL_P_swing==1):
            units= 2
            L=25
            componentlist.append(["COR-3725","Sash Extension","90-90",L,units])
        elif(MDL_SP_SP==1):
            L=25
            units=4
            componentlist.append(["COR-3725","Sash Extension","90-90",L,units])
        if(jamb_type=="ADJ"):
            componentlist.append(["COR-3740","Adjustable Jamb","90-90",shutter_height+45,2])
        if(Wall_SP_lock+MDL_P_swing==1):
            units=1
            componentlist.append(["COR-3741","Sliding Post","90-90",shutter_height+45,units])
        elif(MDL_SP_SP==1):
            units=2
            componentlist.append(["COR-3741","Sliding Post","90-90",shutter_height+45,units])
        if(MDL_D_swing==1):
            componentlist.append(["COR-3742","Lock Keeper Adaptor","90-90",shutter_height,2])
        if(MDL_D_swing+MDL_P_swing+MDL_H_swing==1):
            units=2
            L=shutter_height
            shape="90-90"
            componentlist.append(["COR-3743","Swing Door Lock Adaptor",shape,L,units])
        if(Wall_HR_lock+MDL_H_swing==1):
            units=2
            L=shutter_height
            componentlist.append(["COR-3744","Half Roller Adaptor","90-90",L,units])
        elif(MDL_HR_HR==1):
            units=4
            L=shutter_height
            componentlist.append(["COR-3744","Half Roller Adaptor","90-90",L,units])
        if(Wall_swing+Wall_SP_lock==1):
            units=1
            L=shutter_height+24
            componentlist.append(["COR-3745","Swing Door Rebate Shutter","90-90",L,units])
        elif(MDL_D_swing+MDL_SP_SP+MDL_P_swing+MDL_H_swing==1):
            units=2
            L=shutter_height+24
            componentlist.append(["COR-3745","Swing Door Rebate Shutter","90-90",L,units])
        if(jamb_type=='ADJ' and (Wall_swing+Wall_SP_lock)):
            L=shutter_height+45
            units=1
            shape='90-90'
            componentlist.append(["COR-3746","Swing Door Rebate Adj Jamb",shape,L,units])


        componentlist.append(["COR-3780","19mm Glazing bead",'90-90',shutter_height-100,(left+right)*2])
        componentlist.append(["COR-3780","19mm Glazing bead",'90-90',shutter_width-70,(left+right)*2])
        if(sill_type=='LTH-1'):
            componentlist.append(["COR-3790","Threshold NTB",'90-90',length,1])
        if(sill_type=='LTH-2'):
            componentlist.append(["COR-3789","Threshold TB",'90-90',length,1])
        if(length>1000):
            if(jamb_type=="ADJ"):
                L=length-70-43
            else:
                L=length-70
            componentlist.append(["COR-4503","Track Rail",'90-90',L,1])
        accesslist=[]
        if(height>=2850):
            hinge_per_leaf=6
        elif(height>=2450):
            hinge_per_leaf=5
        elif(height>=1900):
            hinge_per_leaf=4
        else:
            hinge_per_leaf=3
        if(opening=="OUT"):
            isout=1
        else:
            isout=0
        if(left==0 or right==0):
            units=hinge_per_leaf
            for i in range(1,left+right):
                if(i%2==0):
                    units=units+(hinge_per_leaf-2)
                else:
                    units=units+(hinge_per_leaf-isout)
        else:
            units=2*hinge_per_leaf
            print(units)
            for i in range(1,left):
                if(i%2==0):
                    units=units+(hinge_per_leaf-2)
                    print(hinge_per_leaf-2)
                else:
                    units=units+(hinge_per_leaf-isout)
                    print((hinge_per_leaf-isout))
            for i in range(1,right):
                if(i%2==0):
                    units=units+(hinge_per_leaf-2)
                    print(hinge_per_leaf-2)
                else:
                    units=units+(hinge_per_leaf-isout)
                    print((hinge_per_leaf-isout))
                
        accesslist.append(["COR-363720","Standard Hinges",units])
        accesslist.append(["COR-353725","Handle Hinges Out",left_pair+right_pair])
        accesslist.append(["COR-363721","Bottom Roller",int((left-2)/2)+int((right-2)/2)])
        accesslist.append(["COR-363722","Top Guide",int((left-2)/2)+int((right-2)/2)])
        if(MDL_P_swing):
            accesslist.append(["COR-363723","S/P Bottom Roller",1]) 
            accesslist.append(["COR-363724","S/P Top Guide",1])
        if((left%2==0)and bool_roller):
            accesslist.append(["COR-403720","Half Roller Left",1])
            accesslist.append(["COR-403722","Half Guide Left",1])            
        if((right%2==0)and bool_roller):
            accesslist.append(["COR-403721","Half Roller Right",1])  
            accesslist.append(["COR-403723","Half Roller Left",1]) 
        return componentlist,accesslist
        
    else:
        logger.error("La and Ha Not Within Limits")
        raise UserError("La and Ha Not Within Limits")
    
    
cost_list = [
    ['COR-3789',6500,1],
    ['COR-3730',6500,2],
    ['COR-3721',6500,3],
    ['COR-3725',6500,4],
    ['COR-3780',6500,5],
    ['COR-3745',6500,6],
    ['COR-3743',6500,7],
    ['COR-3742',6500,8],
    ['COR-3745',6500,9],
    ['COR-3740',6500,10],
    ['COR-3746',6500,11],
    ['COR-4503',6500,12],
    ['COR-3741',6500,13],
    ['COR-3731',6500,14],
]

def total_cost(component_list,materials_list=cost_list):
    quantity={}
    p_units=1
    result=[]
    for component in component_list:
        # print("Total number of "+i.name+" of length "+ str(i.length)+" required = "+str(i.unit*p_units) )
        quantity[component.material_reference]=quantity.get(component.material_reference,0)+component.units*p_units*component.length    
    total=0

    reference_names = component_list.mapped('material_reference')
    for material in materials_list:
        if material[0] in reference_names:
    # for i,j in materials_list.items():
            units=math.ceil(quantity[material[0]]/material[1])
            total=total+(units*material[2])
            # print(j.name)
            # print( str(units)+" units "+ j.name+ " cost - AED "+ str(units*j.cost))
            result.append([material[0],units,material[2],units*material[2],material[1]*units-(quantity[material[0]])])
        # result.append((total))
    # print('\n Total Cost - ', sum(total))
    return result

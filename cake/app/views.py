from urllib import request

from django.shortcuts import render, redirect

# Create your views here.

from django.views import View


from .models import Cake,Wishlist,Cart

from .forms import CakeForm

from django.db.models import Q

from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from authentication.custom_permissions import allowed_roles




# @method_decorator(login_required(login_url='login'), name = 'dispatch')

class HomeView(View):

    template = 'cake/home.html'

    page = 'Home'

    

    def get(self,request,*args,**kwargs):

        # Cakes = Cake.objects.all()

        Cakes = Cake.objects.filter(active_status=True)

        birthday_cakes = Cakes.filter(category__name='Birthday Cakes')  

        wedding_cakes = Cakes.filter(category__name='Wedding Cakes')  
        
        plum_cakes = Cakes.filter(category__name='Plum Cakes')  
        
        muffins = Cakes.filter(category__name='Muffins')  

        query = request.GET.get('query')

        search_results = None

        if query:

            search_results = Cakes.filter(Q (name__icontains=query) | 
                                          Q  (description__icontains=query) |
                                          Q  (category__name__icontains=query) |
                                          Q  (shape__name__icontains=query) |
                                          Q  (weight__name__icontains=query) |
                                          Q  (flavour__name__icontains=query) 
                                          )
        data = {'page':self.page,'cakes':Cakes,'birthday_cakes':birthday_cakes,'wedding_cakes':wedding_cakes,'plum_cakes':plum_cakes,'muffins':muffins,'search_results':search_results,'query':query}

        return render(request,self.template,context=data)
    

# class AddCakeView(View):
#     template = 'cake/add-cake.html'

#     page = 'Add Cake'

#     def get(self,request,*args,**kwargs):

#         data = {'page':self.page}

#         return render(request,self.template,context=data)

#     def post(self,request,*args,**kwargs):

#         name = request.POST.get('name')

#         description = request.POST.get('description')
        
#         photo = request.FILES.get('photo')

#         category = request.POST.get('category')

#         flavour = request.POST.get('flavour')

#         shape = request.POST.get('shape')   

#         weight = request.POST.get('weight')

#         egg_added = request.POST.get('egg_added')       

#         is_availability = request.POST.get('is_available')

#         price = request.POST.get('price')

#         # print(name,description,photo,category,flavour,shape,weight,egg_added,is_availability,price)

#         Cake.objects.create(name=name,description=description,photo=photo,category=category,
#                             flavour=flavour,shape=shape,weight=weight,egg_added=egg_added,
#                             is_available=is_availability,price=price)
        

#         return redirect('home')

@method_decorator(allowed_roles(['Admin']),name ='dispatch')
class AddCakeView(View):

    template = 'cake/add-cake.html'

    page = 'Add Cake'

    form_class = CakeForm

    def get(self,request,*args,**kwargs):

        form = self.form_class()

        data = {'page':self.page,'form': form}

        return render(request,self.template,context=data)

    def post(self,request,*args,**kwargs):

         form =  self.form_class(request.POST,request.FILES)

         if form.is_valid ():

             form.save()   

             return redirect('home')
    
         data = {'form':form, 'page':self.page }

         return render(request,self.template,context=data)

class CakeDetailsView(View):

    template = 'cake/cake-details.html'

    def get (self,request,*args,**kwargs):    


        uuid = kwargs.get('uuid')

        cake = Cake.objects.get(uuid=uuid)

        data = {'cake':cake}

        return render(request,self.template,context=data)



@method_decorator(allowed_roles(['Admin']),name ='dispatch')
class CakeEditView(View):

     template = 'cake/edit-cake.html'

     page = 'Edit Cake'

     form_class = CakeForm

     def get (self,request,*args,**kwargs):
         
         uuid = kwargs.get('uuid')

         cake = Cake.objects.get(uuid=uuid)
         
         form = self.form_class(instance=cake)

         data = {'form':form}

         return render(request,self.template,context=data)  
     

     def post(self,request,*args,**kwargs):
         
         uuid = kwargs.get('uuid')

         cake = Cake.objects.get(uuid=uuid)

         form = self.form_class(request.POST,request.FILES,instance=cake)

         if form.is_valid():
             
             form.save()

             return redirect('cake-details',uuid=cake.uuid)
         
         data = {'form':form,'page':self.page}

         return render(request,self.template,context=data)
      

@method_decorator(allowed_roles(['Admin']),name ='dispatch')
class CakeDeleteView(View):

    # hard delete - permanently delete the record from database

    # def get (self,request,*args,**kwargs):

    #    uuid = kwargs.get('uuid')

    #    cake = Cake.objects.get(uuid=uuid)

    #    cake.delete() 

    #    return redirect('home') 


    # soft delete - just change the status of the record to inactive

    def get (self,request,*args,**kwargs):

       uuid = kwargs.get('uuid')

       cake = Cake.objects.get(uuid=uuid)

       cake.active_status = False

       cake.save() 

       return redirect('home') 



@method_decorator(allowed_roles(['User']),name ='dispatch')
class AddToWishList(View):

    def get (self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        cake = Cake.objects.get(uuid=uuid)

        wishlist = Wishlist.objects.get(user=request.user)

        wishlist.cakes.add(cake)

        return redirect('home')
    

@method_decorator(allowed_roles(['User']),name ='dispatch')    
class RemoveFromWishList(View):

     def get (self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        cake = Cake.objects.get(uuid=uuid)

        wishlist = Wishlist.objects.get(user=request.user)

        wishlist.cakes.remove(cake)

        return redirect('home')
        
@method_decorator(allowed_roles(['User']),name ='dispatch') 
class WishListView(View):

    template = 'cake/wishlist.html'


    def get (self,request,*args,**kwargs):

        wishlist_items = request.user.wishlist.cakes.all() 

        data = {'wishlist_items':wishlist_items }

        return render (request,self.template,context=data)
    

@method_decorator(allowed_roles(['User']),name ='dispatch')
class AddToCart(View):

    def get (self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        cake = Cake.objects.get(uuid=uuid)

        cart = Cart.objects.get(user=request.user)

        cart.cakes.add(cake)

        return redirect('home')

@method_decorator(allowed_roles(['User']),name ='dispatch')    
class RemoveFromCart(View):

     def get (self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        cake = Cake.objects.get(uuid=uuid)

        Cart = Cart.objects.get(user=request.user)

        Cart.cakes.remove(cake)

        return redirect('home')
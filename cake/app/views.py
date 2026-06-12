from django.shortcuts import render,redirect

# Create your views here.

from django.views import View

from .models import Cake,Wishlist,Cart,Order,DeliveryAddress

from .forms import CakeForm,DeliveryAddressForm

from django.db.models import Q

from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from authentication.custom_permission import allowed_roles

from cake.utility import generate_order_id

from payment.models import Payment

from django.contrib import messages

# @method_decorator(login_required(login_url='login'),name='dispatch')

class HomeView(View):

    template = 'cake/home.html'

    page = 'Home'

    
    def get(self,request,*args,**kwargs):

        # cakes = Cake.objects.all()

        cakes = Cake.objects.filter(active_status=True)

        birthday_cakes = cakes.filter(category__name = 'Birthday Cakes')

        wedding_cakes = cakes.filter(category__name = 'Wedding Cakes')

        plum_cakes = cakes.filter(category__name = 'Plum Cakes')

        muffins = cakes.filter(category__name = 'Muffins')

        query = request.GET.get('query')

        search_results = None

        if query :

            search_results = cakes.filter(Q(name__icontains=query) |
                                          Q(description__icontains=query)|
                                          Q(category__name__icontains=query)|
                                          Q(shape__name__icontains=query)|
                                          Q(weight__name__icontains=query)|
                                          Q(flavour__name__icontains=query)
                                          
                                          )

        data = {'page' : self.page,'cakes':cakes,'birthday_cakes' : birthday_cakes,'wedding_cakes' :wedding_cakes,'plum_cakes':plum_cakes,'muffins':muffins ,'search_results':search_results,'query':query}

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

#         is_available = request.POST.get('is_available')

#         price = request.POST.get('price')

#         # print(name,description,photo,category,flavour,shape,weight,egg_added,is_available,price)

#         Cake.objects.create(name=name,description=description,photo=photo,category=category,flavour=flavour,shape=shape,weight=weight,egg_added=egg_added,is_available=is_available,price=price)

#         return redirect('home')

@method_decorator(allowed_roles(['Admin']),name='dispatch')
class AddCakeView(View):

    template = 'cake/add-cake.html'

    page = 'Add Cake'

    form_class = CakeForm

    def get(self,request,*args,**kwargs):

        form = self.form_class()

        data = {'page':self.page,'form':form}

        return render(request,self.template,context=data)
    
    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST,request.FILES)

        if form.is_valid():

            form.save()

            messages.success(request,'Cake Created Successfully')
  
            return redirect('home')
        
        data = {'form': form,'page':self.page}

        return render(request,self.template,context=data)

class CakeDetailsView(View):

    template = 'cake/cake-details.html'

    page = 'Cake-Details'

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        cake = Cake.objects.get(uuid=uuid)

        data = {'page': self.page ,'cake':cake}

        return render(request,self.template,context=data)
    
@method_decorator(allowed_roles(['Admin']),name='dispatch')
class CakeEditedView(View):

        template = 'cake/edit-cake.html'

        page = 'Edit Cake'

        form_class = CakeForm

        def get(self,request,*args,**kwargs):

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

                messages.success(request,'Cake Updated Successfully')

                return redirect('cake-details',uuid=cake.uuid)
            
            data = {'form':form,'page':self.page}

            return render(request,self.template,context=data)

@method_decorator(allowed_roles(['Admin']),name='dispatch')       
class CakeDeleteView(View):

    # ....hard delete 

    # def get(self,request,*args,**kwargs):

    #     uuid = kwargs.get('uuid')

    #     cake = Cake.objects.get(uuid=uuid)

    #     cake.delete()

    #     return redirect('home')

    # .... soft delete

    
    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        cake = Cake.objects.get(uuid=uuid)

        cake.active_status = False

        cake.save()

        messages.success(request,'Cake Deleted Successfully')

        return redirect('home')
    
@method_decorator(allowed_roles(['User']),name='dispatch')       
class AddToWishList(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        cake = Cake.objects.get(uuid=uuid)

        wishlist = Wishlist.objects.get(user=request.user)

        wishlist.cakes.add(cake)

        messages.success(request,'Cake Added')

        return redirect('home')
    
@method_decorator(allowed_roles(['User']),name='dispatch')       
class RemoveFromWishList(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        cake = Cake.objects.get(uuid=uuid)

        wishlist = Wishlist.objects.get(user=request.user)

        wishlist.cakes.remove(cake)

        return redirect('home')
    
@method_decorator(allowed_roles(['User']),name='dispatch')       
class WishlistView(View):

    template = 'cake/wishlist.html'

    page = 'Wishlist'

    def get(self,request,*args,**kwargs):

        wishlist_items = request.user.wishlist.cakes.all()

        data = {'page':self.page,'wishlist_items':wishlist_items}

        return render(request,self.template,context=data)

@method_decorator(allowed_roles(['User']),name='dispatch')       
class AddToCart(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        cake = Cake.objects.get(uuid=uuid)

        cart = Cart.objects.get(user=request.user)

        cart.cakes.add(cake)

        messages.success(request,'Cake Added')

        return redirect('home')

@method_decorator(allowed_roles(['User']),name='dispatch')       
class RemoveFromCart(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        cake = Cake.objects.get(uuid=uuid)

        cart = Cart.objects.get(user=request.user)

        cart.cakes.remove(cake)

        return redirect('home')
    
@method_decorator(allowed_roles(['User']),name='dispatch')       
class CheckoutView(View):

    template = 'cake/checkout.html'

    page = 'checkout'

    def get(self,request,*args,**kwargs):

        user = request.user

        order_id = generate_order_id()

        cakes = request.user.cart.cakes.all()

        cakes_ids = cakes.values_list('id',flat=True)

        total_price = request.user.cart.get_total

        already_order = Order.objects.filter(user=user,cakes__in=cakes_ids,order_placed=False)

        if already_order.exists():
            
            order = already_order.first()

        else:

            order = Order.objects.create(user=user,order_id=order_id,total_price=total_price)

            order.cakes.add(*cakes)

        data = {'page':self.page, 'order':order}

        return render(request,self.template,context=data)
    
class PlaceOrderView(View):

    def post(self,request,*args,**kwargs):

       order_uuid = kwargs.get('uuid')

       address_uuid = request.POST.get('address_uuid')

       payment_method = request.POST.get('payment')

       order = Order.objects.get(uuid=order_uuid)

       address = DeliveryAddress.objects.get(uuid=address_uuid)

       order.delivery_address = address

       order.payment_option = payment_method

       order.save()

       payment_exists = Payment.objects.filter(order=order)

       if payment_exists.exists():
           
           payment = payment_exists.first()

       else :
           
           payment = Payment.objects.create(order=order,amount=order.total_price)

       if payment_method == 'Online':
           
           return redirect('razorpay',uuid=payment.uuid)

       return redirect('home')



@method_decorator(allowed_roles(['User']), name='dispatch')
class AddDeliveryAddressView(View):

    template = 'cake/add-address.html'

    page = 'Add Delivery Address'

    def get(self, request, *args, **kwargs):

        form = DeliveryAddressForm()

        data = {'page':self.page,'form': form}

        return render(request, self.template, context=data)

    def post(self, request, *args, **kwargs):

        form = DeliveryAddressForm(request.POST)

        if form.is_valid():

            address = form.save(commit=False)

            address.user = request.user

            address.save()

            messages.success(request, 'Address Added Successfully')

            return redirect('address-list')

        data = {'form': form}

        return render(request, self.template, context=data)


@method_decorator(allowed_roles(['User']), name='dispatch')
class DeliveryAddressListView(View):

    template = 'cake/address-list.html'

    page = 'Delivery Address'

    def get(self, request, *args, **kwargs):

        addresses = DeliveryAddress.objects.filter(user=request.user)

        data = {'page':self.page, 'addresses': addresses}

        return render(request, self.template, context=data)


@method_decorator(allowed_roles(['User']), name='dispatch')
class UpdateDeliveryAddressView(View):

    template = 'cake/add-address.html'

    page = 'Update Delivery Address'

    def get(self, request, *args, **kwargs):

        uuid = kwargs.get('uuid')

        address = DeliveryAddress.objects.get(uuid=uuid,user=request.user)

        form = DeliveryAddressForm(instance=address)

        data = {'page':self.page, 'form': form}

        return render(request, self.template, context=data)

    def post(self, request, *args, **kwargs):

        uuid = kwargs.get('uuid')

        address = DeliveryAddress.objects.get(uuid=uuid,user=request.user)

        form = DeliveryAddressForm(request.POST,instance=address)

        if form.is_valid():

            form.save()

            messages.success(request, 'Address Updated Successfully')

            return redirect('address-list')

        data = {'form': form}

        return render(request, self.template, context=data)
    

@method_decorator(allowed_roles(['user']), name='dispatch')
class DeleteDeliveryAddressView(View):

    def get(self, request, *args, **kwargs):

        uuid = kwargs.get('uuid')

        address = DeliveryAddress.objects.get(uuid=uuid,user=request.user)

        address.delete()

        messages.success(request, 'Address Deleted Successfully')

        return redirect('address-list')
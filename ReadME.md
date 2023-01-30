# MeAnalytics for Resturants

Tables
    - CustomerInfo
        - Phone number (unique) (len==10)
        - Name
        - Customer id (primary key)
        
    - Order
        - Order id (primary key)
        - Quantity of item ordered
        - Item id (foreign key)
        - Order cost
        - Date
        - customer id (foreign key)
        
    - UserRatings
        - Order id (primary & foreign key)
        - Rating given
        
    - FoodItems
        - Item id (primary key)
        - Item price
        - Item name
        - Item rating
        - Number of times orderd
        - Availability

Endpoints
    User
        - ShowMenu
        - PlacingOrder
        - GivingRating
        - Signup/Login
        - OrderCancel
        - TodaysMostOrdered
        - OrderHistory
    Owner
        - TodaysSale
        - AddNewFoodItem
        - ChangeFoodAvailibility
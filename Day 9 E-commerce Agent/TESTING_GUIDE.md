# Testing Guide - Day 9 E-commerce Agent

## Quick Start Testing

### 1. Start the Services

**Terminal 1 - API Server:**
```bash
cd "Day 9 E-commerce Agent\backend"
python src/api_server.py
```
Wait for: `API will be available at: http://localhost:8000`

**Terminal 2 - Frontend:**
```bash
cd "Day 9 E-commerce Agent\frontend"
pnpm dev
```
Wait for: `Ready on http://localhost:3000`

**Terminal 3 - Voice Agent (Optional):**
```bash
cd "Day 9 E-commerce Agent\backend"
python src/agent.py dev
```

### 2. Run Automated Tests

**Terminal 4 - Test Script:**
```bash
cd "Day 9 E-commerce Agent\backend"
python test_cart_checkout.py
```

Expected output:
```
🧪 Testing E-commerce API Cart & Checkout Functionality

1️⃣ Testing empty cart...
   ✅ Empty cart test passed

2️⃣ Testing add to cart...
   ✅ Add to cart test passed

...

🎉 ALL TESTS PASSED!
```

## Manual Testing Checklist

### Frontend Testing (http://localhost:3000)

#### ✅ Product Catalog
- [ ] Products load correctly
- [ ] Search bar filters products
- [ ] Category tabs filter products
- [ ] Product cards show all information

#### ✅ Add to Cart
- [ ] Click "Add to Cart" on any product
- [ ] Button shows checkmark briefly
- [ ] Cart badge updates with item count
- [ ] Cart total updates

#### ✅ View Cart
- [ ] Click cart button in top-right
- [ ] Cart sidebar opens
- [ ] All items are listed
- [ ] Quantities are correct
- [ ] Total is calculated correctly

#### ✅ Remove from Cart
- [ ] Click X button on cart item
- [ ] Item is removed immediately
- [ ] Total updates
- [ ] Cart count updates

#### ✅ Checkout
- [ ] Add items to cart
- [ ] Click "Checkout" button
- [ ] Success message appears
- [ ] Cart is cleared
- [ ] Order ID is shown

#### ✅ Error Handling
- [ ] Try checkout with empty cart → Shows error
- [ ] Network error → Shows error alert

### Voice Agent Testing

#### ✅ Browse Products
```
You: "Show me electronics"
Agent: Should list electronics products

You: "Browse clothing"
Agent: Should list clothing items
```

#### ✅ Search Products
```
You: "Search for iPhone"
Agent: Should find iPhone products with IDs

You: "Find a frying pan"
Agent: Should find cookware items

You: "Look for moisturizer"
Agent: Should find skincare products
```

#### ✅ Add to Cart
```
You: "Add phone-001 to cart"
Agent: "Great! I've added 1 iPhone 15 Pro to your cart..."

You: "Add 2 of laptop-001"
Agent: Should add 2 laptops to cart
```

#### ✅ View Cart
```
You: "What's in my cart?"
Agent: Should list all cart items with quantities and total

You: "Show my cart"
Agent: Should display cart contents
```

#### ✅ Remove from Cart
```
You: "Remove phone-001 from cart"
Agent: Should remove item and show updated total
```

#### ✅ Checkout
```
You: "Checkout my cart"
Agent: "Order placed successfully! Order ID: xxx..."

You: "Place my order"
Agent: Should create order and clear cart
```

#### ✅ Order History
```
You: "Show my last order"
Agent: Should display most recent order details
```

#### ✅ Error Scenarios
```
You: "Checkout" (with empty cart)
Agent: "Your cart is empty. Please add items before checking out."

You: "Add invalid-id to cart"
Agent: "Sorry, I couldn't find a product with ID 'invalid-id'..."
```

## API Testing (Using curl or Postman)

### Get Catalog
```bash
curl http://localhost:8000/acp/catalog
```

### Get Categories
```bash
curl http://localhost:8000/acp/categories
```

### Add to Cart
```bash
curl -X POST http://localhost:8000/acp/cart/add \
  -H "Content-Type: application/json" \
  -d '{"product_id": "phone-001", "quantity": 1, "session_id": "test"}'
```

### View Cart
```bash
curl http://localhost:8000/acp/cart?session_id=test
```

### Remove from Cart
```bash
curl -X POST http://localhost:8000/acp/cart/remove \
  -H "Content-Type: application/json" \
  -d '{"product_id": "phone-001", "session_id": "test"}'
```

### Checkout
```bash
curl -X POST http://localhost:8000/acp/cart/checkout \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test", "buyer": {"name": "Test", "email": "test@example.com"}}'
```

### Get Orders
```bash
curl http://localhost:8000/acp/orders
```

## Common Issues & Solutions

### Issue: Products not loading
**Solution:** 
- Check API server is running on port 8000
- Check browser console for CORS errors
- Verify `commerce.py` has product data

### Issue: Cart not updating
**Solution:**
- Check session_id consistency
- Verify API responses in Network tab
- Check browser console for errors

### Issue: Checkout fails
**Solution:**
- Ensure cart has items
- Check API server logs
- Verify order creation in `orders.json`

### Issue: Voice agent not responding
**Solution:**
- Check LiveKit server is running
- Verify API keys in `.env.local`
- Check agent logs for errors

## Performance Testing

### Load Testing
```bash
# Test with multiple concurrent requests
for i in {1..10}; do
  curl -X POST http://localhost:8000/acp/cart/add \
    -H "Content-Type: application/json" \
    -d "{\"product_id\": \"phone-001\", \"quantity\": 1, \"session_id\": \"user$i\"}" &
done
wait
```

### Response Time Testing
```bash
# Measure API response time
time curl http://localhost:8000/acp/catalog
```

## Test Data

### Sample Product IDs
- `phone-001` - iPhone 15 Pro (INR 134,900)
- `laptop-001` - MacBook Air M3 (INR 114,900)
- `headphones-001` - AirPods Pro 2 (INR 24,900)
- `cookware-001` - Non-Stick Frying Pan (INR 2,499)
- `skincare-002` - Moisturizing Face Cream (INR 1,499)

### Sample Session IDs
- `default` - Default session
- `web_user` - Frontend user session
- `test` - Test session

## Success Criteria

All tests should pass:
- ✅ All automated tests pass
- ✅ All frontend buttons work
- ✅ All voice commands work
- ✅ Error handling works correctly
- ✅ Cart persists across page refreshes
- ✅ Orders are created successfully
- ✅ No console errors

## Reporting Issues

If you find issues:
1. Check browser console for errors
2. Check API server logs
3. Check agent logs (if using voice)
4. Note the exact steps to reproduce
5. Check if issue is in frontend, backend, or agent

## Next Steps

After testing:
1. Review `CART_CHECKOUT_FIXES.md` for implementation details
2. Check `orders.json` for created orders
3. Check `carts.json` for cart state
4. Review logs for any warnings

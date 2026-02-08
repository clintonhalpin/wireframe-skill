# Flow: Boutique Hotel Booking

## Flow Diagram

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Search &     │     │  Room        │     │ Date & Room  │
│ Browse       ├────▶│  Detail      ├────▶│ Selection    │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                 │        
                                                 ▼        
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│              │     │              │     │    Guest     │
│ Confirmation │◀────┤  Payment     │◀────┤ Information  │
│              │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
```

Screens to wireframe:

1. Search & Browse — User filters by date/location and browses property cards
2. Room Detail — User views room info, amenities, and pricing
3. Date & Room Selection — User picks dates and room type
4. Guest Information — User enters personal details and requests
5. Payment — User enters payment and reviews order
6. Confirmation — User sees booking reference and next steps

## Screens

### Step 1: Search & Browse

```
┌────────────────────────────────────────────────────┐
│  ████████████████████████                          │
├────────────────────────────────────────────────────┤
│                                                    │
│  Location              Check-in       Check-out    │
│  [________________]    [__________]   [__________] │
│                                                    │
│  Guests [2 v]   [ Search ]                         │
│                                                    │
├────────────────────────────────────────────────────┤
│  ▒▒▒▒▒▒▒▒▒ results     Sort by [Recommended v]     │
│                                                    │
│  ┌──────────────────────┐  ┌──────────────────────┐│
│  │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │  │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │  │
│  │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │  │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │  │
│  │ ████████████████     │  │ ████████████████     ││
│  │ ▒▒▒▒▒▒ · ▒▒▒▒▒      │  │ ▒▒▒▒▒▒ · ▒▒▒▒▒      │  │
│  │ ░░░░░░░░░░░░░░░░    │  │ ░░░░░░░░░░░░░░░░    │  │
│  │          ▒▒▒▒▒▒/night│  │          ▒▒▒▒▒▒/night││
│  │        [View Room]   │  │        [View Room]   ││
│  └──────────────────────┘  └──────────────────────┘│
│                                                    │
│  ┌──────────────────────┐  ┌──────────────────────┐│
│  │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │  │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │  │
│  │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │  │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │  │
│  │ ████████████████     │  │ ████████████████     ││
│  │ ▒▒▒▒▒▒ · ▒▒▒▒▒      │  │ ▒▒▒▒▒▒ · ▒▒▒▒▒      │  │
│  │ ░░░░░░░░░░░░░░░░    │  │ ░░░░░░░░░░░░░░░░    │  │
│  │          ▒▒▒▒▒▒/night│  │          ▒▒▒▒▒▒/night││
│  │        [View Room]   │  │        [View Room]   ││
│  └──────────────────────┘  └──────────────────────┘│
│                                                    │
└────────────────────────────────────────────────────┘
```

User searches by location and dates, browses a card grid of available properties with images, ratings, and nightly rates.

---

### Step 2: Room Detail

```
┌────────────────────────────────────────────────────┐
│  < Back to Results                                 │
├────────────────────────────────────────────────────┤
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     │
├────────────────────────────────────────────────────┤
│                                                    │
│  ██████████████████████████                        │
│  ▒▒▒▒▒▒ · ▒▒▒▒▒▒▒▒                                 │
│                                                    │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░     │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░     │
│                                                    │
│  AMENITIES                                         │
│  ░░░░░░░  ░░░░░░░  ░░░░░░░  ░░░░░░░                │
│  ░░░░░░░  ░░░░░░░  ░░░░░░░                         │
│                                                    │
├────────────────────────────────────────────────────┤
│  ▒▒▒▒▒▒/night                     [ Book Now ]     │
└────────────────────────────────────────────────────┘
```

User views the room's hero image, description, amenity list, and per-night price, then taps Book Now to continue.

---

### Step 3: Date & Room Selection

```
┌────────────────────────────────────────────────────┐
│  Select Dates & Room             Step 1 of 4       │
├────────────────────────────────────────────────────┤
│                                                    │
│  CHECK-IN                  CHECK-OUT               │
│  ┌──────────────────┐     ┌──────────────────┐     │
│  │ < ▒▒▒▒▒▒▒▒▒▒▒ > │     │ < ▒▒▒▒▒▒▒▒▒▒▒ > │       │
│  │ Mo Tu We Th Fr Sa│     │ Mo Tu We Th Fr Sa│     │
│  │ ░░ ░░ ░░ ░░ ░░ ░░│     │ ░░ ░░ ░░ ░░ ░░ ░░│     │
│  │ ░░ ░░ ░░ ░░ ░░ ░░│     │ ░░ ░░ ░░ ░░ ░░ ░░│     │
│  │ ░░ ░░ ░░ ░░ ░░ ░░│     │ ░░ ░░ ░░ ░░ ░░ ░░│     │
│  │ ░░ ░░ ░░ ░░ ░░ ░░│     │ ░░ ░░ ░░ ░░ ░░ ░░│     │
│  └──────────────────┘     └──────────────────┘     │
│                                                    │
│  ROOM TYPE                                         │
│  (*) Standard         ▒▒▒▒▒▒/night                 │
│  ( ) Deluxe           ▒▒▒▒▒▒/night                 │
│  ( ) Suite            ▒▒▒▒▒▒/night                 │
│                                                    │
│  Guests  [2 adults v]                              │
│                                                    │
│  ▒▒ nights · ▒▒▒▒▒▒ total         [ Continue ]     │
└────────────────────────────────────────────────────┘
```

User selects check-in/check-out dates from calendar pickers, chooses a room type, and sees the total before continuing.

---

### Step 4: Guest Information

```
┌────────────────────────────────────────────────────┐
│  Guest Information                 Step 2 of 4     │
├────────────────────────────────────────────────────┤
│                                                    │
│  First Name              Last Name                 │
│  [____________________]  [____________________]    │
│                                                    │
│  Email Address                                     │
│  [____________________________________________]    │
│                                                    │
│  Phone Number                                      │
│  [____________________________________________]    │
│                                                    │
│  Special Requests                                  │
│  [____________________________________________]    │
│  [____________________________________________]    │
│  [____________________________________________]    │
│                                                    │
│  Arrival Time                                      │
│  [3:00 PM – 4:00 PM                          v]    │
│                                                    │
│               < Back         [ Continue ]          │
└────────────────────────────────────────────────────┘
```

User enters name, contact info, special requests, and estimated arrival time.

---

### Step 5: Payment

```
┌────────────────────────────────────────────────────┐
│  Payment                           Step 3 of 4     │
├───────────────────────────┬────────────────────────┤
│                           │  BOOKING SUMMARY       │
│  CARD DETAILS             │                        │
│                           │  ░░░░░░░░░░░░░░░░░░    │
│  Cardholder Name          │  ▒▒▒▒▒▒▒▒ – ▒▒▒▒▒▒▒▒   │
│  [_______________________]│  ▒▒ nights             │
│                           │                        │
│  Card Number              │  Room         ▒▒▒▒▒▒   │
│  [_______________________]│  Taxes        ▒▒▒▒▒▒   │
│                           │  ────────────────────  │
│  Exp Date       CVC       │  Total        ▒▒▒▒▒▒   │
│  [___________]  [_____]   │                        │
│                           │                        │
│  [x] Save card for future │                        │
│                           │                        │
│      < Back               │                        │
│      [ Confirm Booking ]  │                        │
└───────────────────────────┴────────────────────────┘
```

User enters payment details alongside the booking summary showing dates, nights, and total cost.

---

### Step 6: Confirmation

```
┌────────────────────────────────────────────────────┐
│                                                    │
│             Booking Confirmed!                     │
│                                                    │
│       ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░            │
│       Confirmation #▒▒▒▒▒▒▒▒                       │
│                                                    │
├────────────────────────────────────────────────────┤
│                                                    │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░                    │
│  ▒▒▒▒▒▒▒▒ room                                     │
│                                                    │
│  Check-in:   ▒▒▒▒▒▒▒▒▒▒▒▒                          │
│  Check-out:  ▒▒▒▒▒▒▒▒▒▒▒▒                          │
│  Guests:     ▒▒▒▒▒▒▒▒                              │
│  Total Paid: ▒▒▒▒▒▒▒▒                              │
│                                                    │
│         [ Add to Calendar ]                        │
│                                                    │
└────────────────────────────────────────────────────┘
```

User sees the confirmed booking with reference number, stay dates, and an option to add the trip to their calendar.

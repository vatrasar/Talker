---
name: Talker
platform: Python / Flet
colors:
  surface: '#0b1326'
  surface_dim: '#0b1326'
  surface_bright: '#31394d'
  surface_container_lowest: '#060e20'
  surface_container_low: '#131b2e'
  surface_container: '#171f33'
  surface_container_high: '#222a3d'
  surface_container_highest: '#2d3449'
  on_surface: '#dae2fd'
  on_surface_variant: '#bbc9cf'
  inverse_surface: '#dae2fd'
  inverse_on_surface: '#283044'
  outline: '#859399'
  outline_variant: '#3c494e'
  surface_tint: '#4cd6ff'
  primary: '#a4e6ff'
  on_primary: '#003543'
  primary_container: '#00d1ff'
  on_primary_container: '#00566a'
  inverse_primary: '#00677f'
  secondary: '#b7c8e1'
  on_secondary: '#213145'
  secondary_container: '#3a4a5f'
  on_secondary_container: '#a9bad3'
  tertiary: '#ceddf6'
  on_tertiary: '#233144'
  tertiary_container: '#b3c1da'
  on_tertiary_container: '#414f64'
  error: '#ffb4ab'
  on_error: '#690005'
  error_container: '#93000a'
  on_error_container: '#ffdad6'
  background: '#0b1326'
  on_background: '#dae2fd'
typography:
  headline_lg:
    size: 32
    weight: 'bold'
    letter_spacing: -0.5
  headline_md:
    size: 24
    weight: 'bold'
    letter_spacing: -0.2
  headline_sm:
    size: 18
    weight: 'w500'
  body_lg:
    size: 16
    weight: 'normal'
  body_md:
    size: 14
    weight: 'normal'
  label_md:
    size: 12
    weight: 'w500'
    letter_spacing: 0.5
spacing:
  xs: 4
  sm: 8
  md: 16
  lg: 24
  xl: 48
borderRadius:
  sm: 2
  md: 4
  lg: 8
  xl: 12
---

# Talker Design System (Python Flet)

## Brand & Style

The design system is anchored in the concept of **Calculated Precision**, specifically optimized for the **Python Flet** framework. It is designed for high-performance users who require a tool that feels like an extension of their workflow. The aesthetic is a fusion of **Corporate Modern** and **Minimalism**, prioritizing functional clarity over decorative flourish.

The interface should evoke a sense of calm authority and deep focus. By utilizing a dark-themed, low-fatigue palette punctuated by high-energy accents, the system facilitates long-form creative or analytical tasks.

## Colors & Theme

The palette is built for Flet's `Theme` and `ColorScheme` architecture. Use hex strings for custom color definitions in `flet.Theme`.

* **Primary (Electric Blue):** Used for `ElevatedButton`, active `NavigationRail` icons, and focus indicators.
* **Secondary (Slate Gray):** Utilized for non-interactive structural elements and secondary labels.
* **Surface Layering:** Use `surface_container` variants to define visual hierarchy. Flet `Container` controls should use these colors to indicate depth.

## Typography

Flet `Text` controls should utilize the following styles (mapped to `flet.TextStyle`). The system recommends the **Geist** font (load via `page.fonts`).

* **Headlines:** Bold weights with tight letter spacing for a "compact" look.
* **Body:** Optimized for readability using `flet.TextStyle(size=14, weight=ft.FontWeight.NORMAL)`.
* **Labels:** Use for metadata, often in `ft.FontWeight.W500` with slight tracking.

## Layout & Spacing

Flet-native layout logic:

* **Sidebar:** Use `ft.NavigationRail` (width: 240) or a custom `ft.Column` within a `ft.Container`.
* **Main Content:** Use `ft.Column` or `ft.ListView` with `spacing=16` (`md`) and `padding=ft.padding.all(24)` (`lg`).
* **Grid:** Use `ft.ResponsiveRow` for the main content area to handle different window sizes.
* **Standard Spacing:** Use the `spacing` units (4, 8, 16, 24) for `padding`, `margin`, and `spacing` properties of Flet controls.

## Elevation & Depth

In Flet, depth is achieved through `Container.bgcolor` shifts (Tonal Layering) and `Container.shadow`.

* **Level 0 (Background):** `ft.colors.BACKGROUND` or `#0B1326`.
* **Level 1 (Surface):** `ft.colors.SURFACE_VARIANT`. Used for sidebars.
* **Level 2 (Containers):** Cards and inputs. Use `ft.border.all(1, ft.colors.OUTLINE_VARIANT)` and `border_radius=4`.
* **Level 3 (Overlays):** Modals and Popups. Use `ft.BoxShadow` with `blur_radius=24` and `spread_radius=0`.

## Shapes & Radius

Flet uses the `border_radius` property for most controls.

* **Buttons & Inputs:** `border_radius=4` (`md`).
* **Cards & Large Containers:** `border_radius=8` (`lg`).
* **Icons:** Use `ft.Icon` with geometric sets like `ft.icons.SHIELD_OUTLINED`.

## Components (Flet Implementation)

### Buttons

* **Primary:** `ft.ElevatedButton` or `ft.FilledButton` with `style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4))`.
* **Secondary:** `ft.OutlinedButton` with `side=ft.BorderSide(1, ft.colors.OUTLINE)`.
* **Tertiary:** `ft.TextButton`.

### Input Fields

* **TextField:** `ft.TextField(border_color=ft.colors.OUTLINE, focused_border_color=ft.colors.PRIMARY, border_radius=4, filled=True)`.

### Lists & Navigation

* **NavigationRail:** `selected_label_style` and `unselected_label_style` should match the typography spec.
* **ListTile:** Use `ft.ListTile` for navigation items with `hover_color` set to a low-opacity slate.

### Data Tables

* **DataTable:** `ft.DataTable` with `heading_row_color`, `divider_thickness=1`, and `horizontal_lines_color`.
